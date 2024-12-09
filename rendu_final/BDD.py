import mysql.connector
from datetime import datetime

# Se connecter à la base de données
def get_connection():
    conn = mysql.connector.connect(
        host='34.155.104.207',
        user='Worker',
        password='N7kvgIRRouGPq2',
        database='todolist',
        port=3306
    )
    return conn

# Charger les tâches depuis la base de données
def load_tasks(user_id, cursor, sort_column='priorite', sort_order=True):
    valid_columns = ['id', 'titre', 'description', 'date_creation', 'echeance', 'priorite', 'statut']
    if sort_column not in valid_columns:
        raise ValueError("Invalid sort column")
    
    order = 'ASC' if sort_order else 'DESC'
    query = f"SELECT id, titre, description, date_creation, echeance, priorite, statut FROM taches WHERE user_id = %s ORDER BY {sort_column} {order}"
    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    return tasks

# Fonction pour afficher les tâches triées par priorité croissante
def afficher_tache_prio_croissant(user_id, window, cursor):
    tasks = load_tasks(user_id, cursor, sort_column='priorite', sort_order=True)
    task_values = [list(task[1:]) for task in tasks]
    if window:  # Vérifie que window est bien défini
        window['-TASK_LIST-'].update(values=task_values)
        window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Fonction pour afficher les tâches triées par priorité décroissante
def afficher_tache_prio_decroissant(user_id, window, cursor):
    tasks = load_tasks(user_id, cursor, sort_column='priorite', sort_order=False)
    task_values = [list(task[1:]) for task in tasks]
    if window:  # Vérifie que window est bien défini
        window['-TASK_LIST-'].update(values=task_values)
        window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Affiche les tâches triées par échéance croissante
def afficher_tache_echeance_croissant(user_id, window, cursor):
    tasks = load_tasks(user_id, cursor, sort_column='echeance', sort_order=True)
    task_values = [list(task[1:]) for task in tasks]
    window['-TASK_LIST-'].update(values=task_values)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Affiche les tâches triées par échéance décroissante
def afficher_tache_echeance_decroissant(user_id, window, cursor):
    tasks = load_tasks(user_id, cursor, sort_column='echeance', sort_order=False)
    task_values = [list(task[1:]) for task in tasks]
    window['-TASK_LIST-'].update(values=task_values)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Affiche les tâches triées par date de création croissante
def afficher_tache_date_croissant(user_id, window, cursor):
    tasks = load_tasks(user_id, cursor, sort_column='date_creation', sort_order=True)
    task_values = [list(task[1:]) for task in tasks]
    window['-TASK_LIST-'].update(values=task_values)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Affiche les tâches triées par date de création décroissante
def afficher_tache_date_decroissant(user_id, window, cursor):
    tasks = load_tasks(user_id, cursor, sort_column='date_creation', sort_order=False)
    task_values = [list(task[1:]) for task in tasks]
    window['-TASK_LIST-'].update(values=task_values)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')

# Affiche les tâches treiés par ID
def afficher_tache_default(user_id, window, cursor):
    """
    Affiche les tâches triées par ID dans l'interface graphique.
    Cette fonction est appelée au démarrage pour initialiser la liste des tâches.
    """
    tasks = load_tasks(user_id, cursor, sort_column='id', sort_order=True)
    task_values = [list(task[1:]) for task in tasks]  # Exclut l'ID dans l'affichage
    window['-TASK_LIST-'].update(values=task_values)
    window['-TASK_COUNT-'].update(f'Tâches restantes : {len(tasks)}')
