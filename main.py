from fastapi import FastAPI, Response
import requests

app = FastAPI()

BASE_URL = "https://xrum.dpdns.org/getPage.php?go=SOLO4EVE"

@app.get("/playlist.m3u")
def generate_playlist():
    try:
        possible_json_urls = [
            f"{BASE_URL}eventi.json",  
            f"{BASE_URL}xrom.json",    
            f"{BASE_URL}list.json",    
            f"{BASE_URL}playlist.json"     
        ]

        data = None

        for url in possible_json_urls:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                break

        if not data:
            return Response("Errore nel recuperare il JSON", status_code=500)

        m3u = "#EXTM3U\n"
        for item in data:
            name = item.get("name", "No Name")
            stream = item.get("url")

            if stream:
                m3u += f'#EXTINF:-1,{name}\n{stream}\n'

        return Response(content=m3u, media_type="audio/x-mpegurl")

    except Exception as e:
        return Response(str(e), status_code=500)
