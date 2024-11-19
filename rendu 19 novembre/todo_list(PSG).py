import PySimpleGUI as sg

# Fonction pour créer la fenêtre
def create_window():
    layout = [
        [sg.Text('Ma To-Do List', font=('Helvetica', 20), justification='center', expand_x=True)],
        [sg.Text('Tâches restantes :', key='-TASK_COUNT-', font=('Helvetica', 10), text_color='blue')],
        [sg.Listbox(values=[], size=(40, 10), key='-TASK_LIST-', select_mode=sg.SELECT_MODE_MULTIPLE)],
        [sg.Button('Ajouter'), sg.Button('Quitter')]
    ]
    return sg.Window('To-Do List', layout, finalize=True)

# Création de la fenêtre
window = create_window()

# Liste des tâches
tasks = []

# Fonction pour mettre à jour la liste des tâches et le compteur
def update_task_list():
    window['-TASK_LIST-'].update(values=tasks)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Boucle principale pour gérer les événements
while True:
    event, values = window.read()

    # Quitter l'application
    if event == sg.WIN_CLOSED or event == 'Quitter':
        break

    # Ajouter une tâche
    if event == 'Ajouter':
        task = sg.popup_get_text('Entrez une nouvelle tâche :', title='Ajouter une tâche')
        if task and task not in tasks:
            tasks.append(task.strip())
            update_task_list()
        elif task in tasks:
            sg.popup('Cette tâche existe déjà !', title='Erreur')
        elif not task:
            sg.popup('Veuillez entrer une tâche valide.', title='Erreur')

# Fermer la fenêtre
window.close()
