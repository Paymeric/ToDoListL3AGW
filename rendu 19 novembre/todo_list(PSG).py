import PySimpleGUI as sg
from datetime import datetime

# Fonction pour créer la fenêtre
def create_window():
    layout = [
        [sg.Text('Ma To-Do List', font=('Helvetica', 30), justification='center', expand_x=True)],
        [sg.Text('Tâches restantes :', key='-TASK_COUNT-', font=('Helvetica', 15), text_color='blue')],
        [sg.Table(values=[], headings=['Nom', 'Description', 'Date de création', 'Échéance', 'Priorité', 'Status'],
                  auto_size_columns=True, justification='left', 
                  col_widths=[30, 45, 22, 22, 15, 15], 
                  key='-TASK_LIST-', row_height=38, expand_x=True)],
        [sg.Button('Ajouter', font=('Helvetica', 12)), sg.Button('Quitter', font=('Helvetica', 12))]
    ]
    return sg.Window('To-Do List', layout, finalize=True, resizable=True, size=(1000, 600))

# Création de la fenêtre
window = create_window()

# Liste des tâches (nom, description, date de création, échéance, priorité, status)
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
        task_name = sg.popup_get_text('Entrez le nom de la tâche :', title='Ajouter une tâche')
        if task_name:
            description = sg.popup_get_text('Entrez la description de la tâche :', title='Description')
            
            # Fenêtre pour entrer l'échéance avec trois champs pour JJ, MM, AAAA
            layout_due_date = [
                [sg.Text('Entrez la date d\'échéance (format JJ/MM/AAAA) :')],
                [sg.Text('Jour :'), sg.InputText('', size=(3, 1), key='-DAY-'), sg.Text('(JJ)', font=('Helvetica', 8))],
                [sg.Text('Mois :'), sg.InputText('', size=(3, 1), key='-MONTH-'), sg.Text('(MM)', font=('Helvetica', 8))],
                [sg.Text('Année :'), sg.InputText('', size=(5, 1), key='-YEAR-'), sg.Text('(AAAA)', font=('Helvetica', 8))],
                [sg.Button('OK')]
            ]
            due_date_window = sg.Window('Choisir l\'échéance', layout_due_date)
            event_due_date, values_due_date = due_date_window.read()
            due_date_window.close()  # Ferme la fenêtre après sélection

            # Récupération des valeurs de date
            day = values_due_date['-DAY-']
            month = values_due_date['-MONTH-']
            year = values_due_date['-YEAR-']
            
            # Vérification que tous les champs sont remplis
            if not (day and month and year):
                sg.popup('Veuillez remplir tous les champs pour la date d\'échéance.', title='Erreur')
                continue  # Retour à l'ajout de la tâche

            # Date d'échéance sous forme "JJ/MM/AAAA"
            due_date = f'{day}/{month}/{year}'
            
            # Fenêtre pour sélectionner la priorité avec un bouton OK
            layout_priority = [
                [sg.Text('Priorité :')],
                [sg.Combo(['1', '2', '3', '4', '5'], default_value='1', key='-PRIORITY-')],
                [sg.Button('OK')]
            ]
            priority_window = sg.Window('Choisir la priorité', layout_priority)
            event_priority, values_priority = priority_window.read()
            priority_window.close()  # Ferme la fenêtre après sélection

            # Récupération de la priorité choisie
            selected_priority = values_priority['-PRIORITY-']

            # Suppression de la pop-up de statut et de la date de création
            # Par défaut, on assigne un statut et une date de création
            status = 'À faire'  # Statut par défaut
            creation_date = datetime.now().strftime('%d/%m/%Y')  # Date de création par défaut

            if task_name and description and due_date and selected_priority:
                # Vérifier si la tâche existe déjà
                task = (task_name.strip(), description.strip(), creation_date, due_date.strip(), selected_priority, status)
                if task not in tasks:
                    tasks.append(task)
                    update_task_list()
                else:
                    sg.popup('Cette tâche existe déjà !', title='Erreur')
            else:
                sg.popup('Veuillez remplir tous les champs.', title='Erreur')

# Fermer la fenêtre principale
window.close()
