class Note:
    def __init__(self, title: str, description: str, priority: int):
        self.title = title
        self.description = description
        self.priority = priority

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_priority(self):
        return self.priority

    def __str__(self):
        return f'---\nНазвание: {self.get_title()}\nОписание: {self.get_description()}\nПриоритет: {self.get_priority()}'
