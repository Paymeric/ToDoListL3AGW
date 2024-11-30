import os
import PySimpleGUI as sg
from datetime import datetime
import mysql.connector
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import threading
from plyer import notification

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="34.155.104.207",
    user="Worker2",
    password="DyFSoW%OvVHn1t7TS^",
    database="todolist"
)

cursor = db.cursor()

# Scopes pour l'API Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Fonction pour se connecter à Google Calendar
def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

# Fonction pour supprimer token.json
def delete_token():
    if os.path.exists('token.json'):
        os.remove('token.json')
        print("token.json supprimé.")

# Fonction pour charger les tâches
def load_tasks(user_id):
    cursor.execute("SELECT id, titre, description, date_creation, echeance, priorite, statut FROM taches WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    return tasks

# Fonction pour exporter les tâches vers Google Calendar (thread secondaire)
def export_to_google_calendar_thread(user_id, window):
    try:
        tasks = load_tasks(user_id)
        service = get_calendar_service()
        for task in tasks:
            title, description, due_date = task[1], task[2], task[4]
            if due_date:
                due_date_str = due_date.strftime('%Y-%m-%d')
                event = {
                    'summary': title,
                    'description': description,
                    'start': {'date': due_date_str},
                    'end': {'date': due_date_str},
                }
                service.events().insert(calendarId='primary', body=event).execute()

        window.write_event_value('EXPORT_DONE', 'Tâches exportées avec succès vers Google Calendar.')

        notification.notify(
            title="Exportation réussie",
            message="Les tâches ont été exportées vers Google Calendar.",
            timeout=10
        )

    except Exception as e:
        window.write_event_value('EXPORT_DONE', f"Erreur d'exportation: {str(e)}")
        notification.notify(
            title="Erreur d'exportation",
            message=f"Une erreur s'est produite : {str(e)}",
            timeout=10
        )

# Fonction principale pour exécuter l'application To-Do List
def run_todo_app(user_id):
    def create_window():
        layout = [
            [sg.Text('Ma To-Do List', font=('Helvetica', 30), justification='center', expand_x=True)],
            [sg.Text('Tâches restantes :', key='-TASK_COUNT-', font=('Helvetica', 15), text_color='blue')],
            [sg.Table(values=[], headings=['Titre', 'Description', 'Date de création', 'Échéance', 'Priorité', 'Statut'],
                      auto_size_columns=True, justification='left',
                      col_widths=[30, 45, 22, 22, 15, 15],
                      key='-TASK_LIST-', row_height=38, expand_x=True, enable_events=True,
                      right_click_menu=['&Menu', ['Supprimer', 'Modifier', 'Marquer comme terminé']])],
            [sg.Button('Ajouter', font=('Helvetica', 12)),
             sg.Button('Exporter vers Google Calendar', font=('Helvetica', 12)),
             sg.Button('Terminer', font=('Helvetica', 12)),
             sg.Button('Quitter', font=('Helvetica', 12))]
        ]
        return sg.Window('To-Do List', layout, finalize=True, resizable=True, size=(1000, 600))

    def update_task_list():
        tasks = load_tasks(user_id)
        task_values = [list(task[1:]) for task in tasks]
        window['-TASK_LIST-'].update(values=task_values)
        window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

    def mark_task_as_done(task_id):
        sql = "UPDATE taches SET statut = 'Terminée' WHERE id = %s"
        cursor.execute(sql, (task_id,))
        db.commit()
        update_task_list()

    window = create_window()
    update_task_list()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Quitter':
            delete_token()
            break

        if event == 'Ajouter':
            layout_add_task = [
                [sg.Text('Titre de la tâche :'), sg.InputText(key='-TASK_TITLE-')],
                [sg.Text('Description :'), sg.Multiline(size=(40, 5), key='-TASK_DESCRIPTION-')],
                [sg.Text('Date d\'échéance (JJ/MM/AAAA) :')],
                [sg.Text('Jour :'), sg.Input(size=(4, 1), key='-DAY-'),
                 sg.Text('Mois :'), sg.Input(size=(4, 1), key='-MONTH-'),
                 sg.Text('Année :'), sg.Input(size=(6, 1), key='-YEAR-')],
                [sg.Text('Priorité :'), sg.Combo(['1', '2', '3', '4', '5'], default_value='3', key='-PRIORITY-')],
                [sg.Button('Ajouter'), sg.Button('Annuler')]
            ]
            add_task_window = sg.Window('Ajouter une tâche', layout_add_task)

            event_add, values_add = add_task_window.read()
            if event_add in ('Annuler', sg.WIN_CLOSED):
                add_task_window.close()
                continue

            task_name = values_add['-TASK_TITLE-']
            description = values_add['-TASK_DESCRIPTION-']
            day, month, year = values_add['-DAY-'], values_add['-MONTH-'], values_add['-YEAR-']
            priority = values_add['-PRIORITY-']

            try:
                due_date = f'{year}-{month}-{day}'
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                sg.popup('Format de date incorrect.', title='Erreur')
                add_task_window.close()
                continue

            if not all([task_name, description, day, month, year, priority]):
                sg.popup('Tous les champs sont obligatoires.', title='Erreur')
                add_task_window.close()
                continue

            creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = 'À faire'
            cursor.execute(
                "INSERT INTO taches (titre, description, echeance, priorite, statut, date_creation, user_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (task_name, description, due_date, priority, status, creation_date, user_id)
            )
            db.commit()
            update_task_list()
            add_task_window.close()

            notification.notify(
                title="Tâche ajoutée",
                message=f"Tâche '{task_name}' ajoutée avec succès.",
                timeout=10
            )

        if event == 'Terminer':
            selected_task = values['-TASK_LIST-']
            if selected_task:
                selected_row_index = selected_task[0]
                tasks = load_tasks(user_id)
                task_id = tasks[selected_row_index][0]
                mark_task_as_done(task_id)
            else:
                sg.popup('Veuillez sélectionner une tâche.', title='Erreur')

        if event == 'Exporter vers Google Calendar':
            threading.Thread(target=export_to_google_calendar_thread, args=(user_id, window), daemon=True).start()

        if event == 'EXPORT_DONE':
            sg.popup(values[event], title='Succès')

        if event in ['Supprimer', 'Modifier', 'Marquer comme terminé']:
            selected_task = values['-TASK_LIST-']
            if selected_task:
                selected_row_index = selected_task[0]
                tasks = load_tasks(user_id)
                task_id = tasks[selected_row_index][0]

                if event == 'Supprimer':
                    cursor.execute("DELETE FROM taches WHERE id = %s", (task_id,))
                    db.commit()
                    sg.popup('Tâche supprimée.')
                elif event == 'Modifier':
                    sg.popup('Modification non implémentée.', title='Info')
                elif event == 'Marquer comme terminé':
                    mark_task_as_done(task_id)
                update_task_list()
            else:
                sg.popup('Veuillez sélectionner une tâche.', title='Erreur')

    cursor.close()
    db.close()
    window.close()
