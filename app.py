from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la base de datos
db_connection = psycopg2.connect(
    database="lab_semana03",
    user="postgres",
    password="161049",
    host="localhost",  # Cambiar según tu configuración
    port="5432"  # Puerto por defecto de PostgreSQL
)

@app.route("/", methods=["POST"])
def get_lyrics():
    data = request.get_json()
    song_name = data.get("song_name")

    if song_name:
        cursor = db_connection.cursor()
        cursor.execute("SELECT text FROM music_lyrics WHERE song = %s", (song_name,))
        song_lyrics = cursor.fetchone()
        cursor.close()

        if song_lyrics:
            return jsonify({"lyrics": song_lyrics[0]})
        else:
            return jsonify({"error": "Canción no encontrada"})
    else:
        return jsonify({"error": "Nombre de canción no proporcionado"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
