"""
Proyecto 02 - La voz del socio
Script 02: Limpieza, analisis y generacion de graficos
Autor: Lucas Della Torre | Abril 2026
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from wordcloud import WordCloud, get_single_color_func
import nltk
from nltk.corpus import stopwords
import re
import os
import warnings
warnings.filterwarnings('ignore')

nltk.download('stopwords', quiet=True)

# ============================================================
# CONFIGURACION
# ============================================================

COLORS = {
    'OSDE':          '#005BAC',
    'Swiss Medical': '#D71920',
    'Galeno':        '#F47920',
    'Medife':        '#009490',
    'Medicus':       '#004B8D',
    'Omint':         '#00A651',
    'Sancor Salud':  '#1B4F8A',
}

ORDER = ['OSDE', 'Swiss Medical', 'Galeno', 'Medife', 'Medicus', 'Omint', 'Sancor Salud']

DARK    = '#0B1437'
MUTED   = '#6B7280'
BORDER  = '#E5E7EB'

OUTPUT  = 'assets/charts'
os.makedirs(OUTPUT, exist_ok=True)

plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'font.size':          11,
    'axes.facecolor':     'white',
    'figure.facecolor':   'white',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.spines.left':   False,
    'axes.spines.bottom': True,
    'axes.edgecolor':     BORDER,
    'axes.labelcolor':    MUTED,
    'xtick.color':        MUTED,
    'ytick.color':        MUTED,
    'grid.color':         BORDER,
    'grid.alpha':         0.8,
})

# ============================================================
# CARGA Y LIMPIEZA
# ============================================================

df = pd.read_csv('data/raw_reviews.csv', encoding='utf-8-sig')
print(f"Raw reviews: {len(df)}")

df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', utc=True)
df['fecha'] = df['fecha'].dt.tz_localize(None)
df['anio_mes'] = df['fecha'].dt.to_period('M')

df = df.dropna(subset=['texto'])
df = df[df['texto'].str.strip() != '']

# Normalizar nombre Medife (puede venir con acento)
df['app_name'] = df['app_name'].str.replace('Medifé', 'Medife', regex=False)

df['sentimiento'] = df['rating'].map({
    1: 'Negativo', 2: 'Negativo', 3: 'Neutral', 4: 'Positivo', 5: 'Positivo'
})
df['tiene_respuesta'] = df['respuesta_empresa'].notna() & (df['respuesta_empresa'].str.strip() != '')

df = df[df['app_name'].isin(ORDER)]
PREP_COLORS = [COLORS[p] for p in ORDER]

print(f"Reviews limpias: {len(df)}")
print(df['app_name'].value_counts().reindex(ORDER).to_string())

# ============================================================
# CHART 01 — Rating promedio por prepaga
# ============================================================

avg = df.groupby('app_name')['rating'].mean().reindex(ORDER)
global_avg = avg.mean()

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(ORDER, avg.values, color=PREP_COLORS, height=0.55, zorder=3)
ax.axvline(global_avg, color=DARK, linestyle='--', linewidth=1.2, alpha=0.45)
ax.set_xlim(1, 5.8)
ax.set_xlabel('Calificacion promedio (escala 1-5)', fontsize=10)
ax.set_title('Calificacion promedio en Google Play por prepaga', fontsize=13,
             fontweight='bold', color=DARK, pad=14)
ax.invert_yaxis()
ax.xaxis.grid(True, zorder=0)
for bar, val in zip(bars, avg.values):
    ax.text(val + 0.07, bar.get_y() + bar.get_height() / 2,
            f'{val:.2f}', va='center', fontsize=10, fontweight='700', color=DARK)
ax.text(global_avg + 0.06, -0.55,
        f'Promedio global: {global_avg:.2f}', fontsize=8, color=MUTED)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/01_rating_promedio.png', dpi=150, bbox_inches='tight')
plt.close()
print("01 guardado")

# ============================================================
# CHART 02 — Distribucion de estrellas (stacked)
# ============================================================

cnt = df.groupby(['app_name', 'rating']).size().unstack(fill_value=0).reindex(ORDER)
pct = cnt.div(cnt.sum(axis=1), axis=0) * 100

STAR_C = {1: '#DC2626', 2: '#F97316', 3: '#FBBF24', 4: '#4ADE80', 5: '#16A34A'}

fig, ax = plt.subplots(figsize=(11, 5.5))
left = np.zeros(len(ORDER))
for star in [1, 2, 3, 4, 5]:
    if star not in pct.columns:
        continue
    vals = pct[star].values
    bars = ax.barh(ORDER, vals, left=left, color=STAR_C[star], height=0.55,
                   label=f'{star} {"estrella" if star == 1 else "estrellas"}', zorder=3)
    for j, (bar, v) in enumerate(zip(bars, vals)):
        if v > 7:
            ax.text(left[j] + v / 2, bar.get_y() + bar.get_height() / 2,
                    f'{v:.0f}%', ha='center', va='center',
                    fontsize=8, fontweight='700', color='white')
    left += vals

ax.set_xlim(0, 100)
ax.set_xlabel('Porcentaje de reseñas (%)', fontsize=10)
ax.set_title('Distribucion de calificaciones (1 a 5 estrellas)', fontsize=13,
             fontweight='bold', color=DARK, pad=14)
ax.invert_yaxis()
ax.xaxis.grid(True, zorder=0)
ax.legend(loc='lower right', framealpha=0.9, fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/02_distribucion_estrellas.png', dpi=150, bbox_inches='tight')
plt.close()
print("02 guardado")

# ============================================================
# CHART 03 — Sentimiento (positivo / neutral / negativo)
# ============================================================

s = df.groupby(['app_name', 'sentimiento']).size().unstack(fill_value=0).reindex(ORDER)
for col in ['Positivo', 'Neutral', 'Negativo']:
    if col not in s.columns:
        s[col] = 0
sp = s[['Positivo', 'Neutral', 'Negativo']].div(s.sum(axis=1), axis=0) * 100

SENT_C = {'Positivo': '#16A34A', 'Neutral': '#D97706', 'Negativo': '#DC2626'}

fig, ax = plt.subplots(figsize=(11, 5.5))
left = np.zeros(len(ORDER))
for sent in ['Positivo', 'Neutral', 'Negativo']:
    vals = sp[sent].values
    bars = ax.barh(ORDER, vals, left=left, color=SENT_C[sent], height=0.55,
                   label=sent, zorder=3)
    for j, (bar, v) in enumerate(zip(bars, vals)):
        if v > 7:
            ax.text(left[j] + v / 2, bar.get_y() + bar.get_height() / 2,
                    f'{v:.0f}%', ha='center', va='center',
                    fontsize=8.5, fontweight='700', color='white')
    left += vals

ax.set_xlim(0, 100)
ax.set_xlabel('Porcentaje de reseñas (%)', fontsize=10)
ax.set_title('Sentimiento de las reseñas por prepaga', fontsize=13,
             fontweight='bold', color=DARK, pad=14)
ax.invert_yaxis()
ax.xaxis.grid(True, zorder=0)
ax.legend(loc='lower right', framealpha=0.9, fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/03_sentimiento.png', dpi=150, bbox_inches='tight')
plt.close()
print("03 guardado")

# ============================================================
# CHART 04 — Tasa de respuesta de la empresa
# ============================================================

rr = df.groupby('app_name')['tiene_respuesta'].mean().reindex(ORDER) * 100

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(ORDER, rr.values, color=PREP_COLORS, height=0.55, zorder=3)
ax.set_xlim(0, max(rr.values) * 1.3 + 5)
ax.set_xlabel('% de reseñas con respuesta de la empresa', fontsize=10)
ax.set_title('Tasa de respuesta de la empresa a las reseñas', fontsize=13,
             fontweight='bold', color=DARK, pad=14)
ax.invert_yaxis()
ax.xaxis.grid(True, zorder=0)
for bar, val in zip(bars, rr.values):
    ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=10, fontweight='700', color=DARK)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/04_tasa_respuesta.png', dpi=150, bbox_inches='tight')
plt.close()
print("04 guardado")

# ============================================================
# CHART 05 — Evolucion mensual del rating (2024 en adelante)
# ============================================================

df_t = df[df['fecha'] >= '2024-01-01'].copy()
mo = df_t.groupby(['app_name', 'anio_mes'])['rating'].mean().reset_index()
mo['fecha_dt'] = mo['anio_mes'].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(13, 6))
for prep in ORDER:
    sub = mo[mo['app_name'] == prep].sort_values('fecha_dt')
    if len(sub) > 1:
        ax.plot(sub['fecha_dt'], sub['rating'], marker='o', markersize=5,
                linewidth=2.2, color=COLORS[prep], label=prep, alpha=0.9)

ax.set_ylim(1, 5.5)
ax.set_ylabel('Calificacion promedio mensual', fontsize=10)
ax.set_title('Evolucion del rating mensual — Ene 2024 a Abr 2026', fontsize=13,
             fontweight='bold', color=DARK, pad=14)
ax.yaxis.grid(True, zorder=0)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=35, ha='right')
ax.legend(loc='upper left', framealpha=0.9, fontsize=9, ncol=2)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/05_evolucion_mensual.png', dpi=150, bbox_inches='tight')
plt.close()
print("05 guardado")

# ============================================================
# CHART 06 — Menciones a precios y aumentos
# ============================================================

def norm(t):
    return (t.lower()
            .replace('á','a').replace('é','e')
            .replace('í','i').replace('ó','o')
            .replace('ú','u')
            .replace('á','a').replace('é','e')
            .replace('í','i').replace('ó','o')
            .replace('ú','u'))

PRICE_KW = [
    'aumento','aumentaron','aumentar','sube','subio','subio','subira',
    'cara','caro','costosa','costoso','cuota','precio','precios',
    'cuesta','pagar','baja','dar de baja','inflacion','impagable',
    'no puedo pagar','muy caro','muy cara'
]

def has_price(text):
    if pd.isna(text):
        return False
    t = norm(str(text))
    return any(kw in t for kw in PRICE_KW)

df['menciona_precio'] = df['texto'].apply(has_price)
pp = df.groupby('app_name')['menciona_precio'].mean().reindex(ORDER) * 100

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(ORDER, pp.values, color=PREP_COLORS, height=0.55, zorder=3)
ax.set_xlim(0, pp.max() * 1.3 + 3)
ax.set_xlabel('% de reseñas que mencionan precio o aumento', fontsize=10)
ax.set_title('Reseñas que mencionan precios o aumentos (%)', fontsize=13,
             fontweight='bold', color=DARK, pad=14)
ax.invert_yaxis()
ax.xaxis.grid(True, zorder=0)
for bar, val in zip(bars, pp.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=10, fontweight='700', color=DARK)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/06_menciones_precio.png', dpi=150, bbox_inches='tight')
plt.close()
print("06 guardado")

# ============================================================
# CHART 07 — WordClouds por prepaga (reseñas 1-2 estrellas)
# ============================================================

STOP_ES = set(stopwords.words('spanish'))
STOP_EXTRA = {
    'app','aplicacion','prepaga','osde','swiss','medical','galeno',
    'medife','medicus','omint','sancor','salud','bien','mal','hacer',
    'poder','tener','ver','dar','poner','ser','estar','porque','para',
    'que','con','una','uno','como','pero','todo','cuando','hay','vez',
    'cada','solo','ya','ahora','nada','siempre','nunca','favor','buena',
    'bueno','mala','malo','este','esto','esta','son','han','les','sus',
    'desde','hasta','tiene','puede','hace','mejor','peor','igual','misma',
    'mismo','quiero','necesito','veces','muchos','muchas','tambien','asi',
    'aca','ahi','alla','donde','dicha','dicho','algo','alguien','nadie',
    'parte','vez','caso','tipo','forma','manera','tiempo','lugar'
}
STOP_ALL = STOP_ES | STOP_EXTRA

def clean_text(text):
    if pd.isna(text):
        return ''
    t = norm(str(text)).lower()
    t = re.sub(r'[^a-z\s]', ' ', t)
    return ' '.join(w for w in t.split() if w not in STOP_ALL and len(w) > 3)

neg_df = df[df['rating'] <= 2]

fig, axes = plt.subplots(2, 4, figsize=(18, 9))
axes = axes.flatten()

for i, prep in enumerate(ORDER):
    ax = axes[i]
    sub = neg_df[neg_df['app_name'] == prep]
    corpus = ' '.join(sub['texto'].apply(clean_text))

    if len(corpus.strip()) < 100:
        ax.text(0.5, 0.5, 'Datos\ninsuficientes', ha='center', va='center',
                fontsize=12, transform=ax.transAxes, color=MUTED)
        ax.set_title(prep, fontsize=11, fontweight='bold', color=COLORS[prep])
        ax.axis('off')
        continue

    wc = WordCloud(
        width=500, height=300,
        background_color='white',
        color_func=get_single_color_func(COLORS[prep]),
        max_words=60,
        stopwords=STOP_ALL,
        prefer_horizontal=0.85,
        min_font_size=9,
        collocations=False,
    ).generate(corpus)

    ax.imshow(wc, interpolation='bilinear')
    ax.set_title(prep, fontsize=11, fontweight='bold', color=COLORS[prep], pad=8)
    ax.axis('off')

axes[7].axis('off')
fig.suptitle('Palabras mas frecuentes en reseñas negativas (1-2 estrellas)',
             fontsize=15, fontweight='bold', color=DARK, y=1.01)
plt.tight_layout()
plt.savefig(f'{OUTPUT}/07_wordclouds.png', dpi=150, bbox_inches='tight')
plt.close()
print("07 guardado")

# ============================================================
# RESUMEN DE STATS PARA LA LANDING
# ============================================================

print('\n' + '='*60)
print('STATS PARA LA LANDING')
print('='*60)
print(f'\nTotal reseñas: {len(df)}')
print('\n--- Rating promedio ---')
print(avg.round(2).to_string())
print('\n--- Tasa de respuesta (%) ---')
print(rr.round(1).to_string())
print('\n--- % reseñas negativas (1-2 estrellas) ---')
neg_pct = sp['Negativo']
print(neg_pct.round(1).to_string())
print('\n--- % menciones a precios/aumentos ---')
print(pp.round(1).to_string())
total_precio = df['menciona_precio'].sum()
print(f'\nTotal reseñas con mencion de precio: {total_precio} ({total_precio/len(df)*100:.1f}%)')

df.to_csv('data/clean_reviews.csv', index=False, encoding='utf-8-sig')
print('\nDatos limpios guardados en data/clean_reviews.csv')
print('Todos los graficos guardados en assets/charts/')
