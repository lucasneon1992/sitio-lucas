from google_play_scraper import search

prepagas = [
    "OSDE",
    "Swiss Medical",
    "Galeno salud argentina",
    "Medife",
    "Medicus prepaga",
    "Omint salud",
    "Sancor Salud"
]

for query in prepagas:
    print(f"\n=== {query} ===")
    try:
        results = search(query, lang="es", country="ar", n_hits=3)
        for r in results:
            print(f"  ID: {r['appId']}")
            print(f"  Nombre: {r['title']}")
            print(f"  Score: {r.get('score', 'N/A')}")
            print(f"  Installs: {r.get('installs', 'N/A')}")
            print()
    except Exception as e:
        print(f"  Error: {e}")
