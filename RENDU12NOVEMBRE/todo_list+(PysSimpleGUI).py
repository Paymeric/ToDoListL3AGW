import PySimpleGUI as sg

# Fonction pour créer la fenêtre
def create_window():
    layout = [
        [sg.Text('Ma To-Do List', font=('Helvetica', 20), justification='center', expand_x=True)],
        [sg.Text('Tâches restantes :', key='-TASK_COUNT-', font=('Helvetica', 10), text_color='blue')],
        [sg.Listbox(values=[], size=(40, 10), key='-TASK_LIST-', select_mode=sg.SELECT_MODE_MULTIPLE)],
        [sg.InputText('', size=(30, 1), key='-TASK_INPUT-', tooltip='Ajouter une tâche', focus=True),
         sg.Button('Ajouter', bind_return_key=True)],
        [sg.Button('Supprimer'), sg.Button('Marquer comme terminée')],
        [sg.Button('Quitter')]
    ]
    return sg.Window('To-Do List', layout, finalize=True)

# Création de la fenêtre
window = create_window()

# Liste des tâches
tasks = []

# Fonction pour mettre à jour la liste des tâches et le compteur
def update_task_list():
    window['-TASK_LIST-'].update(values=tasks)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len([t for t in tasks if not t.startswith("[Terminé]")])}')

# Boucle principale pour gérer les événements
while True:
    event, values = window.read()
    
    # Quitter l'application
    if event == sg.WIN_CLOSED or event == 'Quitter':
        break
    
    # Ajouter une tâche
    if event == 'Ajouter':
        task = values['-TASK_INPUT-'].strip()
        if task and task not in tasks:
            tasks.append(task)
            update_task_list()
            window['-TASK_INPUT-'].update('')  # Réinitialiser le champ de saisie
        elif task in tasks:
            sg.popup('Cette tâche existe déjà !', title='Erreur')
        else:
            sg.popup('Veuillez entrer une tâche !', title='Erreur')

    # Supprimer une tâche avec confirmation
    if event == 'Supprimer':
        selected_tasks = values['-TASK_LIST-']
        if selected_tasks:
            confirm = sg.popup_yes_no("Êtes-vous sûr de vouloir supprimer la/les tâche(s) sélectionnée(s) ?")
            if confirm == 'Yes':
                for task in selected_tasks:
                    tasks.remove(task)
                update_task_list()
    
    # Marquer comme terminée
    if event == 'Marquer comme terminée':
        selected_tasks = values['-TASK_LIST-']
        if selected_tasks:
            for task in selected_tasks:
                task_index = tasks.index(task)
                if not tasks[task_index].startswith("[Terminé]"):
                    tasks[task_index] = f'[Terminé] {task}'
            update_task_list()

# Fermer la fenêtre
window.close()
