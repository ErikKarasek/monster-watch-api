import requests
from bs4 import BeautifulSoup
import json
import re

def get_monster_deals():
    url = "https://www.kupi.cz/sleva/energeticky-napoj-monster-energy"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Stahuji data z: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Chyba při stahování: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Kupi.cz má data v JSON-LD bloku
    script_tag = soup.find("script", type="application/ld+json")
    if not script_tag:
        print("Nepodařilo se najít JSON data na stránce.")
        return []

    data = json.loads(script_tag.string)
    
    deals = []
    if "offers" in data and "offers" in data["offers"]:
        for offer in data["offers"]["offers"]:
            deal = {
                "obchod": offer.get("offeredBy", "Neznámý"),
                "druh": "Monster Energy (0.5l)", # Základní název
                "cena_akcni": offer.get("price"),
                "cena_puvodni": 42.90, # Odhadovaná běžná cena z textu
                "platnost_do": offer.get("priceValidUntil")
            }
            deals.append(deal)
            
    return deals

if __name__ == "__main__":
    deals = get_monster_deals()
    for d in deals:
        print(f"{d['obchod']}: {d['cena_akcni']} Kč (do {d['platnost_do']})")
