import random

from app.notesList import NotesList
from app.note import Note

if __name__ == "__main__":
    notes = NotesList()
    idx = 1
    while True:
        title = f'Note {idx}'
        description = f'Some description for \'{title}\''
        priority = random.choice([1, 2, 3, 4, 5])
        notes.add_note(Note(title, description, priority))
        idx += 1
        if idx == 5:
            break

    print('\nВаши заметки:')
    for note in notes.get_notes():
        print(note)

    notes.remove_note('Note 1')

    print('\nВаши заметки:')
    for note in notes.get_notes():
        print(note)
