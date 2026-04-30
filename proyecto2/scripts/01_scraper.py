"""
Proyecto 02 — La voz del socio
Script 01: Scraping de reseñas de Google Play Store
Autor: Lucas Della Torre | Abril 2026
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import time
import os

APPS = {
    'OSDE':          'ar.com.osde.ads',
    'Swiss Medical': 'com.swissmedical.clientes',
    'Galeno':        'com.galeno.android',
    'Medifé':        'com.medife.mobile',
    'Medicus':       'com.medicus.mimedicus',
    'Omint':         'ar.com.omint.omint_mobileprepaga_android',
    'Sancor Salud':  'ar.com.sancorsalud.appinstitucional',
}

COUNT_PER_APP = 600

os.makedirs('data', exist_ok=True)

all_reviews = []

for name, app_id in APPS.items():
    print(f"\nScraping {name} ({app_id})...")
    try:
        result, _ = reviews(
            app_id,
            lang='es',
            country='ar',
            sort=Sort.NEWEST,
            count=COUNT_PER_APP,
        )
        for r in result:
            r['app_name'] = name
            r['app_id']   = app_id
        all_reviews.extend(result)
        print(f"  OK {len(result)} resenas obtenidas")
        time.sleep(2)
    except Exception as e:
        print(f"  ✗ Error: {e}")

df = pd.DataFrame(all_reviews)

# Renombrar columnas clave
df = df.rename(columns={
    'userName':     'usuario',
    'content':      'texto',
    'score':        'rating',
    'at':           'fecha',
    'replyContent': 'respuesta_empresa',
    'repliedAt':    'fecha_respuesta',
})

# Columnas útiles
cols = ['app_name', 'app_id', 'usuario', 'rating', 'texto', 'fecha', 'respuesta_empresa', 'fecha_respuesta']
df = df[[c for c in cols if c in df.columns]]

df.to_csv('data/raw_reviews.csv', index=False, encoding='utf-8-sig')
print(f"\n{'='*50}")
print(f"TOTAL: {len(df)} reseñas guardadas en data/raw_reviews.csv")
print(f"\nDistribución por prepaga:")
print(df['app_name'].value_counts().to_string())
