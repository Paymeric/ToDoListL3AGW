from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import secrets
import multiprocessing
import todo  

app = Flask(__name__)


app.secret_key = secrets.token_hex(16)


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


@app.route("/")
def bonjour():
    if 'user_id' in session:
        return render_template("index.html", username=session.get('username'))
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = %s AND mot_de_passe = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['username'] = username 

                
                multiprocessing.Process(target=todo.run_todo_app, args=(user['id'],)).start()

                
                return redirect(url_for('bonjour'))
            else:
                return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect")
        else:
            return "Erreur de connexion à la base de données", 500

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                conn.close()
                return render_template('register.html', error="Cet utilisateur existe déjà.")

        
            cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (%s, %s)', (username, password))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('login'))

        else:
            return "Erreur de connexion à la base de données", 500

    return render_template("register.html")

def run_flask():
    app.run(debug=True, threaded=True)

if __name__ == '__main__':
    run_flask()
