## Pour app.py :
- `pip install flask`
- `pip install mysql-connector-python`

## Pour BDD.py :
- `pip install mysql-connector-python`

## Pour todo.py :
- `pip install mysql-connector-python`
- `pip install PySimpleGUI`
- `pip install google-api-python-client`
- `pip install google-auth-oauthlib`
- `pip install plyer`

---

## Structure du projet

Le code de la ToDoList se compose de 3 fichiers `.py` :
1. **app.py** :  Le service Flask est utilisé pour gérer l'interface web de l'application, connecter les utilisateurs à une base de données de manière sécurisé.
2. **BDD.py** : Fonctions de tri intéragissant avec la base de donnée
3. **todo.py** : L'interface graphique avec PySimpleGUI.

Le projet comprend également 3 fichiers `.html` :
1. **index.html** : La page d’accueil.
2. **login.html** : La page de connexion pour s’authentifier.
3. **register.html** : La page pour créer un compte.

Enfin, il y a un fichier **`credentials.json`** pour interagir avec l'API Google, ici **Google Calendar**.

---

## Responsabilités :

- **Guillaume** : Implémentation de Flask (app.py) ainsi que les fichiers HTML, la fonctionnalité Google Calendar dans l'interface graphique et son bon fonctionnement ainsi que le l'historique des taches.
- **Aymeric** : Ajouter,supprimer,modifier,marquer comme terminé une tâche, déploiement du projet en ligne (incompatible), système de notifications, restaurer une tache depuis l'historique
- **William** : Infrastructure Cloud : Gestion de la création de MySQL dans une instance cloud, Assurer la connectivité à la base de données via l'ajout des adresses IP autorisées.
Base de données : Création des champs et des tables nécessaires
Exception : la table historique n’a pas été réalisée.
Connectivité à la base de données : Configuration et intégration de la connectivité à la base de données dans le code.
Fonctions de tri croissant/décroissant : Implémentation des fonctionnalités de tri en utilisant des requêtes SQL
Import/Export des tâches : Développement des fonctionnalités pour importer et exporter les tâches, Utilisation des fichiers JSON pour sauvegarder et récupérer les données.
Interface graphique : Contribution à la mise en place des boutons dans l’interface, Développement des actions associées aux boutons dans la fonction principale run_todo_app du fichier todo.py.
Debugging : Test du code afin de corriger certaines erreur liées à des modifications
- **Abdel** : Affichage de la premiere fenêtre (Titre,Tableau,Tâches restantes), mise en place de l'appel des fonctions de tri associées, mise en place des bouttons ajouter, supprimer et quitter (hors lien avec la bdd).
