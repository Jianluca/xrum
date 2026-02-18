from fastapi import FastAPI, Response
import requests

app = FastAPI()

BASE_URL = "https://xrum.dpdns.org/getPage.php?go=SOLO-EVENT"

@app.get("/playlist.m3u")
def generate_playlist():
    try:
        possible_json_urls = [
            f"{BASE_URL}eventi.json",  
            f"{BASE_URL}xrom.json",    
            f"{BASE_URL}live.json",    
            f"{BASE_URL}show.json"     
        ]

        data = None

        # Ciclo per cercare il JSON
        for url in possible_json_urls:
            response = requests.get(url, timeout=10)

            # Verifica che la risposta sia corretta e contenga JSON
            if response.status_code == 200:
                try:
                    # Se la risposta è un JSON valido
                    data = response.json()
                    break
                except ValueError:
                    # Se la risposta non è un JSON valido
                    print(f"Errore: la risposta da {url} non è un JSON valido.")
                    continue
            else:
                print(f"Errore: la richiesta a {url} ha restituito lo status {response.status_code}")

        if not data:
            return Response("Errore nel recuperare il JSON", status_code=500)

        # Crea la playlist M3U
        m3u = "#EXTM3U\n"
        for item in data:
            name = item.get("name", "No Name")
            stream = item.get("url")

            if stream:
                m3u += f'#EXTINF:-1,{name}\n{stream}\n'

        return Response(content=m3u, media_type="audio/x-mpegurl")

    except Exception as e:
        return Response(str(e), status_code=500)
