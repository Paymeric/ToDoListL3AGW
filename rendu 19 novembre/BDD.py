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

def ajouter_tache(user_id, titre, description=None, echeance=None, priorite=None):
    conn = get_connection()
    cursor = conn.cursor()

    # Obtenir la date actuelle au format `datetime`
    date_creation = datetime.now()

    # Convertir l'échéance en objet `datetime.date` si elle est fournie
    echeance_date = None
    if echeance:
        try:
            # Supposons que l'échéance est une chaîne au format 'jj/mm/aaaa'
            echeance_date = datetime.strptime(echeance, "%d/%m/%Y").date()
        except ValueError:
            print("Erreur : Format de date incorrect pour l'échéance. Utilisez 'jj/mm/aaaa'.")
            return

    # Exécuter la requête d'insertion
    try:
        cursor.execute('''
            INSERT INTO taches (user_id, titre, description, echeance, priorite, date_creation)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user_id, titre, description, echeance_date, priorite, date_creation))

        conn.commit()
        print("Tâche ajoutée avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion de la tâche : {e}")
    finally:
        cursor.close()
        conn.close()



#Affichage des taches





def afficher_tache_default():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, titre, description, echeance, statut, date_creation
        FROM taches ORDER BY id DESC
    ''',)

    # Récupérer les résultats
    result = cursor.fetchall()

    # Fermer le curseur et la connexion après utilisation
    cursor.close()
    conn.close()

    # Vérifier s'il y a des tâches et les afficher
    if result:
        for row in result:
            id, titre, description, echeance, statut, date_creation = row

            # Formater les dates
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y") if date_creation else "N/A"

            # Afficher les informations de la tâche sans les IDs
            print(f"ID: {id}")
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Statut: {statut}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")




def afficher_tache_echeance_croissant():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT titre, description, echeance, priorite, statut, date_creation
        FROM taches
        ORDER BY echeance ASC
    ''')

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if result:
        for row in result:
            titre, description, echeance, priorite, statut, date_creation = row

            # Formater les dates pour affichage
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y %H:%M:%S") if date_creation else "N/A"

            # Afficher les données
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Priorité: {priorite if priorite else 'N/A'}")
            print(f"Statut: {statut}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")


def afficher_tache_echeance_decroissant():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT titre, description, echeance, priorite, statut, date_creation
        FROM taches
        ORDER BY echeance DESC
    ''')

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if result:
        for row in result:
            titre, description, echeance, priorite, statut, date_creation = row

            # Formater les dates pour affichage
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y %H:%M:%S") if date_creation else "N/A"

            # Afficher les données
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Priorité: {priorite if priorite else 'N/A'}")
            print(f"Statut: {statut}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")


def afficher_tache_date_croissant():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT titre, description, echeance, priorite, statut, date_creation
        FROM taches
        ORDER BY date_creation ASC
    ''')

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if result:
        for row in result:
            titre, description, echeance, priorite, statut, date_creation = row

            # Formater les dates pour affichage
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y %H:%M:%S") if date_creation else "N/A"

            # Afficher les données
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Priorité: {priorite if priorite else 'N/A'}")
            print(f"Statut: {statut}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")


def afficher_tache_date_decroissant():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT titre, description, echeance, priorite, statut, date_creation
        FROM taches
        ORDER BY date_creation DESC
    ''')

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if result:
        for row in result:
            titre, description, echeance, priorite, statut, date_creation = row

            # Formater les dates pour affichage
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y %H:%M:%S") if date_creation else "N/A"

            # Afficher les données
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Priorité: {priorite if priorite else 'N/A'}")
            print(f"Statut: {statut}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")



    
def afficher_tache_priorite_croissant():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT titre, description, echeance, statut, priorite, date_creation FROM taches ORDER BY priorite ASC
    ''',)

    # Récupérer les résultats
    result = cursor.fetchall()

    # Fermer le curseur et la connexion après utilisation
    cursor.close()
    conn.close()

    # Vérifier s'il y a des tâches et les afficher
    if result:
        for row in result:
            titre, description, echeance, statut, priorite, date_creation = row

            # Formater les dates
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y") if date_creation else "N/A"
            # Vérifier la priorité  
            priorite_formatee = priorite if priorite is not None else "N/A"
            # Afficher les informations de la tâche sans les IDs
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Statut: {statut}")
            print(f"Priorité : {priorite_formatee}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")

def afficher_tache_priorite_decroissant():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT titre, description, echeance, statut, priorite, date_creation FROM taches 
        ORDER BY priorite DESC
    ''',)

    # Récupérer les résultats
    result = cursor.fetchall()

    # Fermer le curseur et la connexion après utilisation
    cursor.close()
    conn.close()

    # Vérifier s'il y a des tâches et les afficher
    if result:
        for row in result:
            titre, description, echeance, statut, priorite, date_creation = row

            # Formater les dates
            echeance_formatee = echeance.strftime("%d/%m/%Y") if echeance else "N/A"
            date_creation_formatee = date_creation.strftime("%d/%m/%Y") if date_creation else "N/A"
            # Vérifier la priorité  
            priorite_formatee = priorite if priorite is not None else "N/A"
            # Afficher les informations de la tâche sans les IDs
            print(f"Titre: {titre}")
            print(f"Description: {description}")
            print(f"Échéance: {echeance_formatee}")
            print(f"Statut: {statut}")
            print(f"Priorité : {priorite_formatee}")
            print(f"Date de création: {date_creation_formatee}")
            print("-" * 40)
    else:
        print("Aucune tâche trouvée.")



#Affichage USERS


def afficher_user_default():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM utilisateurs;
    ''',)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if result:
        for row in result:
            print(row)
    else:
        print("Aucun utilisateur trouvée.")



#ajouter_tache(1, 'Vacance', 'Acheter les billets de train', '07/03/2025',2)
#afficher_tache_default() #OK
#afficher_tache_priorite_decroissant() #OK
#afficher_tache_priorite_croissant() #OK
#afficher_user_default()
#ajouter_tache(1, 'Mon Titre', 'Ma Description', '07/03/2026', 3)
#afficher_tache_echeance_decroissant()
#afficher_tache_echeance_croissant()
#afficher_tache_date_decroissant()
afficher_tache_date_croissant()
