from app.notesList import NotesList
from app.note import Note

if __name__ == "__main__":
    notes = NotesList()
    while True:
        title = input('Введите название заметки: ')
        description = input('Введите соджержимое заметки: ')
        priority = int(input('Укажите приоритет (от 1 до 5): '))
        notes.add_note(Note(title, description, priority))
        more = input(
            'Нажмите \'return\' для того чтобы ввести еще одну заметку. \nДля выхода из режима добавленгия заметок введите \'stop\'')
        if more == 'stop':
            break

    print('Ваши заметки:')
    for note in notes.get_notes():
        print(note)

    notes.remove_note('Note 1')

    print('Ваши заметки:')
    for note in notes.get_notes():
        print(note)
