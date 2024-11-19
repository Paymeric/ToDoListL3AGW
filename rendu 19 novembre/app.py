from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import secrets
import threading  # Pour gérer l'interface graphique dans un thread
import todo  # Module pour gérer l'interface graphique PySimpleGUI

app = Flask(__name__)

# Clé secrète pour la gestion des sessions
app.secret_key = secrets.token_hex(16)

# Connexion à la base de données
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='34.155.104.207',
            user='Worker2',
            password='DyFSoW%OvVHn1t7TS^',
            database='todolist'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

# Route pour la page d'accueil
@app.route("/")
def bonjour():
    if 'user_id' in session:  # Si l'utilisateur est connecté
        return render_template("index.html", username=session.get('username'))
    return render_template("index.html")  # Page d'accueil simple si non connecté

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connexion à la base de données et récupération des informations utilisateur
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = %s AND mot_de_passe = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user_id'] = user['id']  # Stocker user_id dans la session
                session['username'] = username  # Stocker le nom d'utilisateur dans la session

                # Lancer l'interface graphique dans un thread
                threading.Thread(target=todo.run_todo_app, args=(user['id'],)).start()

                # Rediriger vers la page d'accueil après connexion réussie
                return redirect(url_for('bonjour'))
            else:
                return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect")
        else:
            return "Erreur de connexion à la base de données", 500

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
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                conn.close()
                return render_template('register.html', error="Cet utilisateur existe déjà.")

            # Ajouter un nouvel utilisateur dans la base de données
            cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (%s, %s)', (username, password))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('login'))

        else:
            return "Erreur de connexion à la base de données", 500

    return render_template("register.html")

# Route pour la déconnexion
@app.route('/logout')
def logout():
    # Supprimer les informations de session pour déconnecter l'utilisateur
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('bonjour'))  # Rediriger vers la page d'accueil

if __name__ == '__main__':
    app.run(debug=True)
