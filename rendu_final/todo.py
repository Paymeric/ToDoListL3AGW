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
import json

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="34.155.104.207",
    user="Worker2",
    password="DyFSoW%OvVHn1t7TS^",
    database="todolist"
)

from BDD import (
    afficher_tache_prio_croissant,
    afficher_tache_prio_decroissant,
    afficher_tache_echeance_croissant,
    afficher_tache_echeance_decroissant,
    afficher_tache_date_croissant,
    afficher_tache_date_decroissant,
    load_tasks,
    afficher_tache_default
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

def update_task_list(user_id,window):
        global tasks
        sort_column = 'priorite'  # Colonne par défaut
        sort_order = True  # Ordre par défaut (croissant)
        tasks = load_tasks(user_id, cursor, sort_column, sort_order)
        task_values = [list(task[1:]) for task in tasks]
        window['-TASK_LIST-'].update(values=task_values)
        window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')
    

def show_task_history(user_id, window):
    cursor.execute("SELECT tache_id, titre, description, echeance, priorite, action, date_modification FROM historique_taches WHERE user_id = %s", (user_id,))
    history = cursor.fetchall()

    layout = [
        [sg.Text('Historique des tâches', font=('Helvetica', 30), justification='center')],
        [sg.Table(
            values=[list(item[1:]) for item in history],
            headings=['Titre', 'Description', 'Priorité', 'Statut', 'Action', 'Date Modification'],
            auto_size_columns=True, justification='left', 
            col_widths=[30, 45, 22, 15, 15, 20],
            key='-HISTORY_LIST-', row_height=38, expand_x=True,
            right_click_menu=['&Menu', ['Restaurer']]  # Option pour restaurer la tâche dans la liste
        )],
        [sg.Button('Fermer')]
    ]

    history_window = sg.Window('Historique des tâches', layout, finalize=True)

    while True:
        event, values = history_window.read()

        if event == sg.WIN_CLOSED or event == 'Fermer':
            history_window.close()
            break

        # Restaurer une tâche de l'historique dans la liste des tâches
        if event == 'Restaurer':
            selected_task = values['-HISTORY_LIST-']
            if selected_task:
                selected_row_index = selected_task[0]
                task_id = history[selected_row_index][0]  # ID de la tâche dans l'historique
                restore_task_from_history(task_id, user_id)  # Appel à la fonction pour restaurer la tâche
                sg.popup('Tâche restaurée', 'La tâche a été réintégrée dans la liste des tâches.')
                update_task_list(user_id,window)  # Mise à jour de l'affichage des tâches dans la fenêtre principale
            else:
                sg.popup('Veuillez sélectionner une tâche.', title='Erreur')
from datetime import datetime

def restore_task_from_history(task_id, user_id):
    # Récupérer la tâche à partir de l'historique
    cursor.execute("SELECT titre, description, echeance, priorite, statut FROM historique_taches WHERE tache_id = %s", (task_id,))
    task = cursor.fetchone()

    # Ensure that the result is consumed (even if we don't need it explicitly)
    cursor.fetchall()  # This will clear any unread results if there are any.

    if task:
        # Récupérer les informations nécessaires pour réinsérer la tâche
        title, description, due_date, priority, status = task

        # Insérer la tâche dans la table principale des tâches
        cursor.execute("""
            INSERT INTO taches (titre, description, echeance, priorite, statut, date_creation, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, description, due_date, priority, status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        db.commit()

        # Supprimer la tâche de l'historique une fois restaurée
        cursor.execute("""
            DELETE FROM historique_taches WHERE tache_id = %s
        """, (task_id,))
        db.commit()

        print("La tâche a été restaurée avec succès !")
    else:
        print("Erreur : Tâche non trouvée dans l'historique.")

# Fonction pour exporter les tâches vers Google Calendar (thread secondaire)
def export_to_google_calendar_thread(user_id, window):
    try:
        tasks = load_tasks(user_id, cursor)  # Inclut le curseur ici
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
        
def exporter_une_tache(task_id, cursor):
    cursor.execute("""
        SELECT titre, description, date_creation, echeance, priorite, statut
        FROM taches WHERE id = %s
    """, (task_id,))
    task = cursor.fetchone()

    if task:
        tache_dict = {
            'titre': task[0],
            'description': task[1],
            'date_creation': str(task[2]),
            'echeance': str(task[3]) if task[3] else None,
            'priorite': task[4],
            'statut': task[5]
        }

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        filename = os.path.join(downloads_path, f"{task[0].replace(' ', '_')}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tache_dict, f, ensure_ascii=False, indent=4)

        sg.popup("Exportation réussie", f"La tâche a été exportée dans :\n{filename}")
    else:
        sg.popup("Erreur", "Impossible de trouver la tâche sélectionnée.")

def importer_une_tache(user_id, window):
    filename = sg.popup_get_file("Sélectionnez un fichier JSON à importer", file_types=(("JSON Files", "*.json"),))
    if not filename:
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            task = json.load(f)

        # Vérifier que le JSON est un dictionnaire unique
        if not isinstance(task, dict):
            raise ValueError("Le fichier JSON doit contenir une seule tâche.")

        # Insérer la tâche dans la base de données
        cursor.execute("""
            INSERT INTO taches (user_id, titre, description, date_creation, echeance, priorite, statut)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            task.get('titre', 'Sans titre'),
            task.get('description', ''),
            task.get('date_creation', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            task.get('echeance', None),
            task.get('priorite', 3),
            task.get('statut', 'À faire')
        ))

        db.commit()
        sg.popup("Importation réussie", "La tâche a été importée avec succès.")
        update_task_list(user_id, window)

    except Exception as e:
        sg.popup("Erreur d'importation", f"{e}")
#----------------------------------------------------------------------------------------------------------------------------------------------
# Fonction principale pour exécuter l'application To-Do List
def run_todo_app(user_id):
    priorite_sort_state = "asc"  # Initialisation de l'état du tri
    global tasks
    sort_column = 'priorite'  # Colonne par défaut pour le tri (priorité)
    sort_order = True  # True pour croissant, False pour décroissant
    notification.notify(
        title="Connexion réussie",
        message="Vous êtes maintenant connecté à votre To-Do List.",
        timeout=10)
    def create_window(): 
        layout = [
            [sg.Text('Ma To-Do List', font=('Helvetica', 30), justification='center', expand_x=True)],
            [sg.Text('Tâches restantes :', key='-TASK_COUNT-', font=('Helvetica', 15), text_color='blue')],
            [sg.Table(
                values=[],
                      headings=['Titre', 'Description', 'Date de création', 'Échéance', 'Priorité', 'Statut'],
                      auto_size_columns=True, justification='left',
                      col_widths=[30, 45, 22, 22, 15, 15],
                      key='-TASK_LIST-', row_height=38, expand_x=True, 
                      enable_events=True, enable_click_events=True)],
            [sg.Button('Ajouter', font=('Helvetica', 12)),
             sg.Button('Exporter vers Google Calendar', font=('Helvetica', 12)),
             sg.Button('Importer', font=('Helvetica', 12)),
             sg.Button('Exporter', font=('Helvetica', 12)),
             sg.Button('Modifier', font=('Helvetica', 12)),
             sg.Button('Supprimer', font=('Helvetica', 12)),
             sg.Button('Terminer', font=('Helvetica', 12)),
             sg.Button('Quitter', font=('Helvetica', 12)),
             sg.Button('Historique des tâches', font=('Helvetica', 12))
            ]

             
        ]
        return sg.Window('To-Do List', layout, finalize=True, resizable=True, size=(1000, 600))

    
    
    def modifier_tache(task_id, user_id, window):
        # Récupérer les informations actuelles de la tâche
        cursor.execute("SELECT titre, description, echeance, priorite FROM taches WHERE id = %s", (task_id,))
        task = cursor.fetchone()

        if task is None:
            sg.popup('La tâche spécifiée n\'existe pas.', title='Erreur')
            return

        # Définir le layout pour la modification
        layout_modify_task = [
            [sg.Text('Modifier la tâche')],
            [sg.Text('Titre:', size=(15, 1)), sg.InputText(task[0], key='-TASK_TITLE-')],
            [sg.Text('Description:', size=(15, 1)), sg.Multiline(task[1], key='-TASK_DESCRIPTION-')],
            [sg.Text('Date d\'échéance (JJ/MM/AAAA):')],
            [sg.Text('Jour:'), sg.Input(size=(4, 1), key='-DAY-', default_text=task[2].day if task[2] else ''),
            sg.Text('Mois:'), sg.Input(size=(4, 1), key='-MONTH-', default_text=task[2].month if task[2] else ''),
            sg.Text('Année:'), sg.Input(size=(6, 1), key='-YEAR-', default_text=task[2].year if task[2] else '')],
            [sg.Text('Priorité:'), sg.Combo(['1', '2', '3', '4', '5'], default_value=str(task[3]), key='-PRIORITY-')],
            [sg.Button('Modifier'), sg.Button('Annuler')]
        ]

        modify_task_window = sg.Window('Modifier une tâche', layout_modify_task)

        while True:
            event, values = modify_task_window.read()

            if event == sg.WIN_CLOSED or event == 'Annuler':
                modify_task_window.close()
                break

            if event == 'Modifier':
                title = values['-TASK_TITLE-']
                description = values['-TASK_DESCRIPTION-']
                day = values['-DAY-']
                month = values['-MONTH-']
                year = values['-YEAR-']
                priority = values['-PRIORITY-']

                # Validation des champs obligatoires
                if not title or not priority:
                    sg.popup('Les champs "Titre" et "Priorité" sont obligatoires.', title='Erreur')
                    continue

                # Validation et formatage de la date
                try:
                    if day and month and year:
                        due_date = f'{year}-{month}-{day}'
                        datetime.strptime(due_date, '%Y-%m-%d')  # Valide le format
                    else:
                        due_date = None  # Aucun changement de date
                except ValueError:
                    sg.popup('Format de date incorrect. Utilisez JJ/MM/AAAA.', title='Erreur')
                    continue

                # Mettre à jour la tâche dans la base de données
                cursor.execute("""
                    UPDATE taches 
                    SET titre = %s, description = %s, echeance = %s, priorite = %s 
                    WHERE id = %s
                """, (title, description, due_date, priority, task_id))
                db.commit()

                sg.popup('Tâche modifiée avec succès.')
                update_task_list(user_id, window)
                modify_task_window.close()
                notification.notify(
                    title="Modification réussie",
                    message=f"La tâche '{title}' a été modifiée avec succès.",
                    timeout=10
                )
                break

    def mark_task_as_done(task_id):
        # Récupérer les informations de la tâche
        cursor.execute("SELECT titre, description, echeance, priorite, statut, user_id FROM taches WHERE id = %s", (task_id,))
        task = cursor.fetchone()

        if task:
            # Ajouter l'historique de la tâche terminée
            cursor.execute("""
                INSERT INTO historique_taches (tache_id, titre, description, echeance, priorite, statut, action, date_modification, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (task_id, task[0], task[1], task[2], task[3], 'Terminée', 'Terminée', datetime.now(), task[5]))
            db.commit()

        # Mettre à jour la tâche comme terminée dans la table principale
        cursor.execute("UPDATE taches SET statut = 'Terminée' WHERE id = %s", (task_id,))
        db.commit()

        update_task_list(user_id,window)

    window = create_window()

    # Appelle afficher_tache_default pour initialiser les tâches avec un tri par ID
    afficher_tache_default(user_id, window, cursor)

    update_task_list(user_id,window)  # Mise à jour initiale des tâches
    

    priorite_sort_state = "asc"  # Initialisation
    echeance_sort_state = "asc"  # Initialement croissant
    date_sort_state = "asc"  # Initialement croissant

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Quitter'):
            delete_token()
            break

        # Gestion du tri des colonnes
        if isinstance(event, tuple) and event[0] == '-TASK_LIST-' and event[2][0] == -1:
            column_index = event[2][1]
            columns = ['titre', 'description', 'date_creation', 'echeance', 'priorite', 'statut']
            if 0 <= column_index < len(columns):
                sort_column = columns[column_index]
                if sort_column == 'date_creation':
                    if date_sort_state == "asc":
                        afficher_tache_date_croissant(user_id, window, cursor)
                        date_sort_state = "desc"
                    else:
                        afficher_tache_date_decroissant(user_id, window, cursor)
                        date_sort_state = "asc"
                elif sort_column == 'echeance':
                    if echeance_sort_state == "asc":
                        afficher_tache_echeance_croissant(user_id, window, cursor)
                        echeance_sort_state = "desc"
                    else:
                        afficher_tache_echeance_decroissant(user_id, window, cursor)
                        echeance_sort_state = "asc"
                elif sort_column == 'priorite':
                    if priorite_sort_state == "asc":
                        afficher_tache_prio_croissant(user_id, window, cursor)
                        priorite_sort_state = "desc"
                    else:
                        afficher_tache_prio_decroissant(user_id, window, cursor)
                        priorite_sort_state = "asc"

        # Ajouter une tâche via fenêtre
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

            while True:
                event_add, values_add = add_task_window.read()
                if event_add in ('Annuler', sg.WIN_CLOSED):
                    add_task_window.close()
                    break

                task_name = values_add['-TASK_TITLE-']
                description = values_add['-TASK_DESCRIPTION-']
                day, month, year = values_add['-DAY-'], values_add['-MONTH-'], values_add['-YEAR-']
                priority = values_add['-PRIORITY-']

                try:
                    due_date = f'{year}-{month}-{day}'
                    datetime.strptime(due_date, '%Y-%m-%d')
                except ValueError:
                    sg.popup('Format de date incorrect.', title='Erreur')
                    continue

                if not all([task_name, description, day, month, year, priority]):
                    sg.popup('Tous les champs sont obligatoires.', title='Erreur')
                    continue

                creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("""
                    INSERT INTO taches (user_id, titre, description, echeance, priorite, statut, date_creation)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, task_name, description, due_date, priority, 'À faire', creation_date))
                db.commit()
                sg.popup('Tâche ajoutée avec succès.')
                update_task_list(user_id, window)
                add_task_window.close()
                break


        # Exporter une tâche sélectionnée
        if event == 'Exporter':
            selected_task = values['-TASK_LIST-']
            if selected_task:
                selected_row_index = selected_task[0]
                tasks = load_tasks(user_id, cursor)
                task_id = tasks[selected_row_index][0]
                exporter_une_tache(task_id, cursor)
            else:
                sg.popup("Veuillez sélectionner une tâche à exporter.", title="Erreur")

        # Importer une tâche depuis un fichier JSON
        if event == 'Importer':
            importer_une_tache(user_id, window)

        # Historique des tâches
        if event == 'Historique des tâches':
            show_task_history(user_id, window)

        # Exporter vers Google Calendar
        if event == 'Exporter vers Google Calendar':
            threading.Thread(target=export_to_google_calendar_thread, args=(user_id, window), daemon=True).start()

        if event == 'EXPORT_DONE':
            sg.popup(values[event], title='Succès')
        
        if event == 'Terminer':
            selected_task = values['-TASK_LIST-']
            if selected_task:
                selected_row_index = selected_task[0]
                tasks = load_tasks(user_id, cursor)
                task_id = tasks[selected_row_index][0]

                # Marquer la tâche comme terminée
                mark_task_as_done(task_id)
                sg.popup("Tâche terminée", "La tâche a été marquée comme terminée.")
                update_task_list(user_id, window)  # Mettre à jour la liste des tâches
            else:
                sg.popup("Veuillez sélectionner une tâche à terminer.", title="Erreur")

        if event in ['Supprimer', 'Modifier']:
            selected_task = values['-TASK_LIST-']
            if selected_task:
                selected_row_index = selected_task[0]
                tasks = load_tasks(user_id,cursor)
                task_id = tasks[selected_row_index][0]

                if event == 'Supprimer':
                    selected_task = values['-TASK_LIST-']
                    if selected_task:
                        selected_row_index = selected_task[0]
                        tasks = load_tasks(user_id, cursor)
                        task_id = tasks[selected_row_index][0]

                        # Récupérer les informations de la tâche avant suppression
                        cursor.execute("SELECT titre, description, echeance, priorite, statut, user_id FROM taches WHERE id = %s", (task_id,))
                        task = cursor.fetchone()

                        if task:
                         # Ajouter l'historique de la tâche supprimée
                            cursor.execute("""
                                INSERT INTO historique_taches (tache_id, titre, description, echeance, priorite, statut, action, date_modification, user_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (task_id, task[0], task[1], task[2], task[3], task[4], 'Supprimée', datetime.now(), task[5]))
                            db.commit()

                        # Supprimer la tâche de la table principale
                        cursor.execute("DELETE FROM taches WHERE id = %s", (task_id,))
                        db.commit()

                        sg.popup('Tâche supprimée.')
                        notification.notify(
                            title="Tâche supprimée",
                            message=f"La tâche '{task[0]}' a été supprimée avec succès.",
                            timeout=10
                        )
                        update_task_list(user_id,window)  # Mise à jour de l'affichage des tâches
                    else:
                        sg.popup('Veuillez sélectionner une tâche.', title='Erreur')
                elif event == 'Modifier':
                    modifier_tache(task_id, user_id, window)

    cursor.close()
    db.close()
    window.close()
