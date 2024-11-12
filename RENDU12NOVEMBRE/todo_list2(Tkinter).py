import tkinter as tk
from tkinter import messagebox

# Fonction pour ajouter une tâche
def add_task():
    task = task_input.get()
    if task and task not in tasks:
        tasks.append(task)
        update_task_listbox()
        task_input.delete(0, tk.END)  # Réinitialiser le champ de saisie
    else:
        messagebox.showwarning("Erreur", "La tâche est vide ou déjà existante.")

# Fonction pour supprimer une tâche
def remove_task():
    selected_tasks = task_listbox.curselection()
    if selected_tasks:
        for task_index in selected_tasks:
            tasks.remove(tasks[task_index])
        update_task_listbox()

# Fonction pour marquer une tâche comme terminée
def mark_as_done():
    selected_tasks = task_listbox.curselection()
    if selected_tasks:
        for task_index in selected_tasks:
            task = tasks[task_index]
            tasks[task_index] = f'[Terminé] {task}'
        update_task_listbox()

# Fonction pour mettre à jour la liste des tâches dans la Listbox
def update_task_listbox():
    task_listbox.delete(0, tk.END)  # Réinitialiser la liste
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Créer la fenêtre principale
window = tk.Tk()
window.title("To-Do List")

# Liste des tâches
tasks = []

# Créer les widgets
title_label = tk.Label(window, text="Ma To-Do List", font=("Helvetica", 20))
title_label.pack(pady=10)

task_listbox = tk.Listbox(window, selectmode=tk.SINGLE, width=40, height=10)
task_listbox.pack(pady=10)

task_input = tk.Entry(window, width=30)
task_input.pack(pady=5)
task_input.insert(0, "Ajouter une tâche...")

add_button = tk.Button(window, text="Ajouter", width=20, command=add_task)
add_button.pack(pady=5)

remove_button = tk.Button(window, text="Supprimer", width=20, command=remove_task)
remove_button.pack(pady=5)

mark_done_button = tk.Button(window, text="Marquer comme terminée", width=20, command=mark_as_done)
mark_done_button.pack(pady=5)

quit_button = tk.Button(window, text="Quitter", width=20, command=window.quit)
quit_button.pack(pady=10)

# Lancer la boucle principale
window.mainloop()
