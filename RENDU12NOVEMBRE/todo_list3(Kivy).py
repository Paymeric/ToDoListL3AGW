from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget


class ToDoApp(App):
    def build(self):
        self.tasks = []  # Liste pour stocker les tâches
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Zone de saisie de la tâche
        self.input_task = TextInput(hint_text="Entrez une tâche", size_hint_y=None, height=40)
        self.layout.add_widget(self.input_task)

        # Bouton pour ajouter la tâche
        self.add_button = Button(text="Ajouter", size_hint_y=None, height=40)
        self.add_button.bind(on_press=self.add_task)
        self.layout.add_widget(self.add_button)

        # ScrollView pour la liste des tâches
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.task_list_layout = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        self.scroll_view.add_widget(self.task_list_layout)

        self.layout.add_widget(self.scroll_view)
        return self.layout

    def add_task(self, instance):
        task_text = self.input_task.text.strip()
        if task_text:
            task_widget = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
            
            # Case à cocher pour marquer la tâche comme terminée
            checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
            checkbox.bind(active=self.toggle_task)
            
            task_label = Label(text=task_text, size_hint_y=None, height=40)
            task_widget.add_widget(checkbox)
            task_widget.add_widget(task_label)
            
            # Ajouter la tâche à la liste
            self.task_list_layout.add_widget(task_widget)

            # Réinitialiser le champ de saisie
            self.input_task.text = ""

    def toggle_task(self, checkbox, value):
        task_label = checkbox.parent.children[0]
        if value:
            task_label.color = (0.5, 0.5, 0.5, 1)  # Gris pour marqué comme terminé
        else:
            task_label.color = (1, 1, 1, 1)  # Blanc pour non terminé


if __name__ == "__main__":
    ToDoApp().run()
