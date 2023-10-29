from app.note import Note


class NotesList:
    def __init__(self):
        self.notes = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def remove_note(self, title: str):
        for i, o in enumerate(self.notes):
            if o.get_title() == title:
                del self.notes[i]
                print(f'Заметка \'{title}\' удалена')
                break
        else:
            print('Такой заметки пока нет')

    def get_notes(self):
        return self.notes
