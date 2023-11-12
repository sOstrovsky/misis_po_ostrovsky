import psycopg2
from flask import request, jsonify

from app.main import app
from .settings import HOST, PORT, SSLMODE, DBNAME, USER, PASSWORD, TARGET_SESSION_ATTRS

connection = psycopg2.connect(f"""
    host={HOST}
    port={PORT}
    sslmode={SSLMODE}
    dbname={DBNAME}
    user={USER}
    password={PASSWORD}
    target_session_attrs={TARGET_SESSION_ATTRS}
""")

SELECT_ALL_NOTES = 'select * from notes;'


@app.route("/api/notes", methods=["GET"])
def get_notes():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_NOTES)
            notes = cursor.fetchall()
            if notes:
                result = []
                for note in notes:
                    result.append({
                        'id': note[0],
                        'title': note[1],
                        'description': note[2],
                        'priority': note[3]
                    })
                return jsonify(result)
            else:
                return jsonify({'error': 'Notes not found.'}), 404


INSERT_NOTE_RETURN_ID = "insert into notes (title, description, priority) values (%s, %s, %s) returning id;"


@app.route("/api/note", methods=["POST"])
def create_note():
    with connection:
        with connection.cursor() as cursor:
            request_data = request.json
            title = str(request_data["title"])
            description = str(request_data["description"])
            priority = int(request_data["priority"])
            cursor.execute(INSERT_NOTE_RETURN_ID, (title, description, priority))
            note_id = cursor.fetchone()[0]
    return jsonify({
        'id': note_id,
        'title': title,
        'description': description,
        'priority': priority
    }), 200


UPDATE_NOTE_BY_ID = 'update notes set title = %s, description = %s, priority = %s where id = %s;'


@app.route("/api/note/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    priority = data["priority"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_NOTE_BY_ID, (title, description, priority, note_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Note with ID {note_id} was not found."}), 404
    return jsonify({"id": note_id, "title": title, "message": f"Note with ID {note_id} successfully updated."}), 200


DELETE_NOTE_BY_ID = 'delete from notes where id = %s'


@app.route("/api/note/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_NOTE_BY_ID, [note_id])
            if cursor.rowcount == 0:
                return jsonify({"error": f"Note with ID {note_id} was not found."}), 404
    return jsonify({"id": note_id, "message": f"Note with ID {note_id} successfully deleted."}), 200
