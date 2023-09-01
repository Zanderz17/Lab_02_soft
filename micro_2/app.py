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
def get_duration():
    data = request.get_json()
    artist = data.get("artist")
    print(artist)

    if artist:
        cursor = db_connection.cursor()
        print("SELECT name, duration_ms FROM songs_2 WHERE artists like {}".format(artist))
        cursor.execute("SELECT name, duration_ms FROM songs_2 WHERE artists like %s", (artist,))
        songs = cursor.fetchall()  # Fetch all rows
        cursor.close()

        if songs:
            songs_data = [{"name": song[0], "duration": song[1]} for song in songs]
            return jsonify({"songs": songs_data})
        else:
            return jsonify({"error": "Canciones no encontradas"})
    else:
        return jsonify({"error": "Nombre de artista no proporcionado"})

if __name__ == "__main__":
    app.run(debug=True, port=7000)
