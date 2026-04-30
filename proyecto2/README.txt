================================================================================
PROYECTO 02 — LA VOZ DEL SOCIO
Lo que revelan 4.200 reseñas sobre la experiencia en el sistema de prepagas argentino
================================================================================

AUTORÍA
-------
Autor: Lucas Della Torre
Perfil: Sociólogo especializado en análisis de datos y Customer Experience (CX)
LinkedIn: https://www.linkedin.com/in/lucasadt/
Sitio web: lucasdellatorre.com
Fecha: Abril 2026

--------------------------------------------------------------------------------

IDEA PRINCIPAL
--------------
La medicina prepaga en Argentina atravesó entre 2024 y 2026 uno de los períodos
más convulsionados de su historia: aumentos acumulados que superaron el 200% en
2024, intervención del gobierno, bajas masivas de socios, y un debate público
permanente sobre si el servicio justificaba el costo.

Este proyecto analiza 4.200 reseñas públicas de las apps de Google Play de siete
prepagas argentinas (OSDE, Swiss Medical, Galeno, Medifé, Medicus, Omint y Sancor
Salud) para responder con datos: ¿qué dice el socio cuando lo escuchan? ¿Dónde
está la fricción? ¿Qué prepagas escuchan y cuáles no? ¿Cómo impactó el contexto
de aumentos en la percepción de los socios?

El análisis se posiciona desde una mirada de Customer Experience (CX): no evalúa
la calidad médica de las prestaciones, sino la experiencia del socio en su
relacionamiento con la empresa, especialmente en el canal digital.

--------------------------------------------------------------------------------

FUENTES DE DATOS
----------------
- Reseñas públicas de Google Play Store (scraping legal de información pública)
- 600 reseñas por prepaga, ordenadas por las más recientes
- Total: 4.200 registros
- Período cubierto: aproximadamente enero 2024 - abril 2026
- Fuente complementaria: noticias de medios argentinos (La Nación, Infobae,
  El Cronista) sobre aumentos de prepagas en 2024-2025

Apps analizadas (package IDs de Google Play):
  - OSDE            → ar.com.osde.ads
  - Swiss Medical   → com.swissmedical.clientes
  - Galeno          → com.galeno.android
  - Medifé          → com.medife.mobile
  - Medicus         → com.medicus.mimedicus
  - Omint           → ar.com.omint.omint_mobileprepaga_android
  - Sancor Salud    → ar.com.sancorsalud.appinstitucional

--------------------------------------------------------------------------------

PASOS Y METODOLOGÍA
-------------------

PASO 1 — Búsqueda y verificación de apps (scripts/00_find_app_ids.py)
  - Se utilizó la función `search()` de google-play-scraper para localizar
    las apps oficiales de cada prepaga en Google Play (país: AR, idioma: es).
  - Los package IDs fueron verificados individualmente con la función `app()`
    para confirmar que correspondían a las apps oficiales.

PASO 2 — Scraping de reseñas (scripts/01_scraper.py)
  - Librería: google-play-scraper (Python)
  - Parámetros: lang='es', country='ar', sort=Sort.NEWEST, count=600
  - El scraping captura: usuario, texto, rating (1-5), fecha, respuesta de la
    empresa y fecha de respuesta.
  - Salida: data/raw_reviews.csv (4.200 filas)

PASO 3 — Limpieza y preprocesamiento (scripts/02_analysis.py)
  - Normalización de fechas (timezone-aware → naive)
  - Eliminación de reseñas vacías o nulas
  - Normalización del nombre "Medifé" → "Medife" para consistencia
  - Clasificación de sentimiento por rating:
      Positivo: 4-5 estrellas
      Neutral:  3 estrellas
      Negativo: 1-2 estrellas
  - Detección de respuesta de la empresa (booleano)
  - Salida: data/clean_reviews.csv

PASO 4 — Análisis exploratorio (scripts/02_analysis.py)
  - Rating promedio por prepaga
  - Distribución porcentual de calificaciones (1 a 5 estrellas)
  - Distribución de sentimiento (positivo/neutral/negativo)
  - Tasa de respuesta de la empresa por prepaga
  - Evolución mensual del rating (período 2024-2026)
  - Menciones a precios/aumentos (diccionario de palabras clave con
    normalización de acentos)

PASO 5 — Análisis de lenguaje natural (scripts/02_analysis.py)
  - Limpieza de texto: minúsculas, eliminación de caracteres no alfabéticos,
    normalización de acentos para matching de stopwords
  - Stopwords: NLTK español + diccionario propio de términos no informativos
    del dominio prepaga
  - WordCloud por prepaga, construida sobre reseñas negativas (1-2 estrellas)
  - Color de cada nube: color oficial de la marca de cada prepaga

PASO 6 — Visualización (scripts/02_analysis.py)
  - Backend: Matplotlib Agg (sin display)
  - Estilo: paleta de colores consistente con los colores de marca de cada
    prepaga a lo largo de todos los gráficos
  - 7 gráficos generados como PNG en assets/charts/

PASO 7 — Construcción de la landing (index.html)
  - HTML/CSS puro, sin frameworks
  - Sistema de diseño del sitio personal: Inter, paleta navy/azul
  - Scroll reveal con Intersection Observer API (sin librerías)
  - Responsive (mobile-first)

--------------------------------------------------------------------------------

TECNOLOGÍA UTILIZADA
--------------------
  Python 3.12.4
  Pandas 2.2.3
  Matplotlib 3.9.0
  Seaborn (visualización complementaria)
  NLTK (stopwords en español)
  WordCloud (nubes de palabras)
  NumPy 2.0.0
  google-play-scraper (scraping de reseñas)
  HTML5 / CSS3 (landing page)
  Power BI (dashboard interactivo — en construcción)

--------------------------------------------------------------------------------

ESTRUCTURA DE ARCHIVOS
----------------------
proyecto2/
├── index.html                          → Landing page del proyecto
├── README.txt                          → Este archivo
├── assets/
│   └── charts/
│       ├── 01_rating_promedio.png      → Rating promedio por prepaga
│       ├── 02_distribucion_estrellas.png
│       ├── 03_sentimiento.png
│       ├── 04_tasa_respuesta.png
│       ├── 05_evolucion_mensual.png
│       ├── 06_menciones_precio.png
│       └── 07_wordclouds.png
├── data/
│   ├── raw_reviews.csv                 → Datos crudos del scraping
│   └── clean_reviews.csv              → Datos limpios post-procesamiento
└── scripts/
    ├── 00_find_app_ids.py             → Búsqueda y verificación de package IDs
    ├── 01_scraper.py                  → Scraping de reseñas Google Play
    └── 02_analysis.py                → Limpieza, análisis y generación de gráficos

--------------------------------------------------------------------------------

RESULTADOS PRINCIPALES
----------------------

Rating promedio (Google Play, escala 1-5):
  Omint          3.48  ★★★☆☆
  Medifé         3.35  ★★★☆☆
  Galeno         3.15  ★★★☆☆
  OSDE           2.90  ★★☆☆☆
  Sancor Salud   1.99  ★★☆☆☆
  Medicus        1.92  ★★☆☆☆
  Swiss Medical  1.90  ★★☆☆☆

Tasa de respuesta de la empresa (% de reseñas respondidas):
  OSDE           90.0%   ← hallazgo destacado
  Medicus        57.7%
  Swiss Medical  47.8%
  Sancor Salud    8.0%
  Galeno          1.0%
  Omint           0.3%
  Medifé          0.0%

% reseñas negativas (1-2 estrellas):
  Swiss Medical  75.7%
  Medicus        75.0%
  Sancor Salud   73.2%
  OSDE           49.3%
  Galeno         42.2%
  Medifé         36.0%
  Omint          34.3%

% reseñas que mencionan precios o aumentos:
  Sancor Salud    9.7%
  Swiss Medical   8.2%
  Medicus         6.2%
  Medifé          5.2%
  OSDE            3.3%
  Omint           3.0%
  Galeno          2.3%
  — Total general: 5.4% (227 de 4.200 reseñas)

--------------------------------------------------------------------------------

HALLAZGOS CLAVE
---------------
1. Swiss Medical, Medicus y Sancor Salud tienen los peores ratings del análisis,
   todos por debajo de 2/5, con más del 70% de sus reseñas en zona negativa. La
   infraestructura médica propia (Swiss Medical, Medicus) no se traduce en mejor
   CX percibido en el canal digital.

2. OSDE lidera la escucha digital con una tasa de respuesta del 90%. Es el único
   actor con una estrategia visible y sistemática de gestión de reseñas en Google
   Play. Sin embargo, su alto nivel de respuesta no se refleja en el mejor rating
   del análisis, lo que sugiere que responder no es suficiente: hay que resolver.

3. Sancor Salud (9.7%) y Swiss Medical (8.2%) son las prepagas donde los socios
   mencionan más frecuentemente precios o aumentos, conectando el contexto
   macroeconómico de 2024 con la experiencia percibida en el canal digital.

4. Omint y Medifé tienen los mejores ratings a pesar de no responder reseñas. Su
   satisfacción parece anclada en la experiencia de atención más que en la
   gestión del canal digital.

5. Los temas dominantes de insatisfacción son transversales al sector: turnos,
   espera, atención telefónica y acceso a la cartilla de prestadores.

6. La tasa de respuesta es un indicador de cultura CX, no de calidad médica.
   La brecha entre escuchar y mejorar es el mayor desafío del sector.

--------------------------------------------------------------------------------

CONTEXTO
--------
El DNU 70/2023 (diciembre 2023) desreguló el mercado de medicina prepaga.
En 2024 las cuotas acumularon aumentos superiores al 200%. El gobierno debió
intervenir en abril-mayo 2024 exigiendo a 7 prepagas reducir sus cuotas hasta
un 33%. Un 5% de los afiliados proyectaba darse de baja; una de las grandes
prepagas reportó pérdida de ~25.000 socios en un año. En 2025 los aumentos
continuaron a un ritmo de 3-3.9% mensual.

--------------------------------------------------------------------------------

ACLARACIONES METODOLÓGICAS
---------------------------
- Este análisis utiliza exclusivamente información pública disponible en Google
  Play Store. No se accedió a datos privados de las empresas.
- Las reseñas reflejan la percepción del canal digital (app) y no
  necesariamente la calidad de la atención médica en sí.
- El sentimiento se clasifica por rating, no por análisis semántico de texto.
  Una reseña de 1 estrella puede contener texto positivo y viceversa.
- Las palabras clave de precio se construyeron con normalización de acentos
  para maximizar la cobertura, pero no capturan todas las formas en que un
  socio puede expresar insatisfacción económica.
- El análisis es descriptivo, no prescriptivo. Los hallazgos no constituyen
  asesoramiento médico ni evaluación de la calidad asistencial.

================================================================================
