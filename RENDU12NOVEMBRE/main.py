import mysql.connector

# Configurer la connexion à la base de données MySQL (utilisation de l'IP publique ou privée de Cloud SQL)
def create_connection():
    db_host = "34.155.104.207"  # Remplacez par l'IP publique ou privée de votre instance Cloud SQL
    db_user = "Worker"  # Remplacez par votre utilisateur MySQL
    db_password = "N7kvgIRRouGPq2"  # Remplacez par votre mot de passe MySQL
    db_name = "todolist"  # Remplacez par le nom de votre base de données

    # Créer la connexion MySQL
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    return conn

# Ajouter une tâche
def add_task(connection, title, description, due_date=None, priority=None):
    cursor = connection.cursor()
    query = """
    INSERT INTO tasks (title, description, due_date, priority)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (title, description, due_date, priority))
    connection.commit()
    print(f"Tâche '{title}' ajoutée.")
    cursor.close()

# Supprimer une tâche
def delete_task(connection, task_id):
    cursor = connection.cursor()
    query = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    connection.commit()
    print(f"Tâche avec ID {task_id} supprimée.")
    cursor.close()

# Modifier une tâche
def edit_task(connection, task_id, title=None, description=None, due_date=None, priority=None):
    cursor = connection.cursor()
    query = "SELECT * FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    task = cursor.fetchone()

    if task:
        update_query = "UPDATE tasks SET "
        values = []

        if title:
            update_query += "title = %s, "
            values.append(title)
        if description:
            update_query += "description = %s, "
            values.append(description)
        if due_date:
            update_query += "due_date = %s, "
            values.append(due_date)
        if priority:
            update_query += "priority = %s, "
            values.append(priority)

        update_query = update_query.rstrip(", ")  # Retirer la dernière virgule
        update_query += " WHERE id = %s"
        values.append(task_id)

        cursor.execute(update_query, tuple(values))
        connection.commit()
        print(f"Tâche avec ID {task_id} modifiée.")
    else:
        print(f"Tâche avec ID {task_id} non trouvée.")
    cursor.close()

# Terminer une tâche
def complete_task(connection, task_id):
    cursor = connection.cursor()
    query = "UPDATE tasks SET status = 'complete' WHERE id = %s"
    cursor.execute(query, (task_id,))
    connection.commit()
    print(f"Tâche avec ID {task_id} marquée comme terminée.")
    cursor.close()

# Afficher les tâches triées par priorité et échéance
def display_tasks(connection):
    cursor = connection.cursor()
    query = """
    SELECT * FROM tasks
    ORDER BY priority DESC, due_date ASC
    """
    cursor.execute(query)
    tasks = cursor.fetchall()

    if tasks:
        print("Liste des tâches :")
        for task in tasks:
            print(f"- {task[1]} | Priorité: {task[4]} | Échéance: {task[3]} | Statut: {task[5]}")
    else:
        print("Aucune tâche à afficher.")
    cursor.close()

# Créer la connexion à la base de données MySQL
connection = create_connection()

if connection:
    # Ajouter des tâches
    add_task(connection, "Acheter du lait", "Acheter 2 litres de lait", due_date="2024-11-13", priority=2)
    add_task(connection, "Réunion", "Réunion avec le client à propos du projet", due_date="2024-11-14", priority=1)

    # Afficher les tâches
    display_tasks(connection)

    # Modifier une tâche
    edit_task(connection, 1, title="Réunion avec le client", priority=3)

    # Marquer une tâche comme terminée
    complete_task(connection, 1)

    # Supprimer une tâche
    delete_task(connection, 2)

    # Afficher à nouveau les tâches
    display_tasks(connection)

    # Fermer la connexion à la base de données
    connection.close()
