# Groupe AGW
- Aymeric Protot
- Guillaume Galinier
- Abdel-Rahim Mezenner
- William El masri boutari 

# To do list noyau minimal :

- Conception de la structure de données pour les tâches et les utilisateurs (BDD).
- Fonctionalités de base pour gérer les tâches (titre, une description, une échéance éventuelle, une priorité éventuelle) : ajouter / supprimer / éditer / terminer une tâche et d'afficher la liste des tâches à faire ordonnées selon la priorité et l'échéance.
- Gestion du stockage des données.
- Interface minimale.


## Idées supplémentaires pour compléter le noyau

- Authentification des utilisateurs.
- Exporter ou importer des tâches 
- Notifications Windows
- Afficher le temps restant pour une tâches.
- historique des tâches finies/supprimées
- Intégration dans des calendriers externes.
- Interface améliorée.

## Dépendances entre les fonctionnalités
L'historique des tâches, exporter et importer des tâches, afficher le temps restant pour une tâche dépendent du noyau principal.
Intégration dans les calendriers externes dépend de tout le reste.
Authentification des utilisateurs et notifications Windows ne dépendent de rien.  

## Priorités
1. Noyau minimal.
2. L'historique des tâches, exporter et importer des tâches, afficher le temps restant.
3. Authentification des utilisateurs et notifications Windows.
4. Intégration dans les calendriers externes dépend de tout le reste.


