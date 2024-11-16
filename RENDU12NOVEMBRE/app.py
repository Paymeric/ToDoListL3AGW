from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connexion à la base de données
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='34.155.104.207',      # Adresse du serveur MySQL
            user='Worker2',             # Utilisateur MySQL
            password='DyFSoW%OvVHn1t7TS^',  # Mot de passe MySQL
            database='todolist'         # Nom de la base de données
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

# Route pour la page d'accueil
@app.route("/")
def bonjour():
    return render_template("index.html")

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connexion à la base de données et récupération des informations utilisateur
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = %s AND mot_de_passe = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                
                return redirect(url_for('home'))  # Si l'utilisateur existe, rediriger vers /home
            
            else:
                return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect")
        else:
            return "Erreur de connexion à la base de données", 500  # Erreur si la connexion échoue

    return render_template('login.html')

# Route pour la page d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                conn.close()
                return "Cet utilisateur existe déjà.", 409  # Code d'erreur 409 pour conflit

            # Ajouter un nouvel utilisateur dans la base de données
            cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (%s, %s)', (username, password))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('login'))  # Rediriger vers la page de connexion

        else:
            return "Erreur de connexion à la base de données", 500  # Erreur si la connexion échoue

    return render_template("register.html")

# Route pour la page d'accueil après connexion
@app.route('/home')
def home():
    # Connexion à la base de données pour afficher les tâches de l'utilisateur connecté
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        # Remplace ici 'user_id' par l'ID réel de l'utilisateur connecté (pour cet exemple, je prends 1)
        cursor.execute('SELECT * FROM taches WHERE user_id = %s', (1,))
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()

        # Affichage des tâches de l'utilisateur dans un tableau
        return render_template("home.html", tasks=tasks)
    else:
        return "Erreur de connexion à la base de données", 500

if __name__ == '__main__':
    app.run(debug=True)
