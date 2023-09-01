from flask import Flask, request, Response, jsonify
import requests
import json

app = Flask(__name__)

# Define mapping of routes to backend services
backend_services = {
    'microservice1': 'http://127.0.0.1:5000/',
    'microservice2': 'http://127.0.0.1:7000/',  # Note the updated port
}

@app.route('/artist-lyrics', methods=['GET'])
def api_gateway():
    artist_name = request.args.get('name')
    backend = 'microservice2'
    
    if backend in backend_services:
        backend_url = backend_services[backend]
        response = requests.post(backend_url, json={"artist": artist_name})
        songs_data = response.json().get("songs")
        
        combined_data = {"artist": artist_name, "songs": []}
        for song in songs_data:
            song_name = song["name"]
            duration = song["duration"]
            
            lyrics_response = requests.post(backend_services['microservice1'], json={"song_name": song_name})
            lyrics = lyrics_response.json().get("lyrics")
            
            song_info = {"name": song_name, "duration": duration, "lyrics": lyrics}
            combined_data["songs"].append(song_info)
        
        # Use json.dumps to format the response with indentation for readability
        prettified_response = json.dumps(combined_data, indent=4)
        
        # Create a Flask Response object with the formatted response
        response = Response(prettified_response, status=200, content_type='application/json')
        response.headers['Content-Disposition'] = 'inline'
        
        return response
    else:
        return Response('Backend not found', status=404)

if __name__ == '__main__':
    app.run(port=5005)