"""
Proyecto 02 - La voz del socio
Script 03: Analisis de topicos mas mencionados en las resenas
Autor: Lucas Della Torre | Abril 2026
"""

import pandas as pd
import re

df = pd.read_csv('data/clean_reviews.csv', encoding='utf-8-sig')

def norm(t):
    if pd.isna(t): return ''
    return (str(t).lower()
            .replace('á','a').replace('é','e')
            .replace('í','i').replace('ó','o')
            .replace('ú','u').replace('ü','u')
            .replace('ñ','n'))

df['texto_norm'] = df['texto'].apply(norm)

TOPICS = {
    'Atencion al cliente':     ['atencion','atienden','atiende','llaman','llamo','llame','espera','espero','demora','demorar','responde','responden','respuesta','servicio','contacto','soporte','comunicar','comunicacion'],
    'Turnos y consultas':      ['turno','turnos','consulta','consultas','cita','especialista','sacar turno','pedir turno','guardia','medico','medica','solicitar turno'],
    'App y plataforma':        ['app','aplicacion','funciona','error','falla','fallo','actualizar','lento','lenta','carga','pantalla','celular','telefono','ingres','usuario','contrasena','login','sesion','tecnico'],
    'Precios y cuotas':        ['precio','precios','cuota','cuotas','aumento','aumentaron','caro','cara','pago','cobro','cobran','factura','sube','subio','valor','costosa','costoso','impagable','plata','dinero'],
    'Cartilla y prestadores':  ['cartilla','prestador','prestadores','clinica','hospital','adherido','profesional','medico','medica','especialista','derivacion','particular','obra social'],
    'Tramites y autorizaciones':['tramite','tramites','autorizacion','autorizaciones','gestion','gestionar','pedido','formulario','documento','documentacion','proceso','burocracia','papel','tramitar'],
    'Cobertura y plan':        ['cobertura','cubre','plan','medicamento','medicamentos','practica','practicas','internacion','cirugia','prestacion','derivar','servicio medico'],
    'Reintegros y facturacion':['reintegro','reintegros','reembolso','devolver','devolucion','cobro indebido','me cobran','factura','nota de credito','acreditar'],
}

total = len(df)
results = {}

for topic, keywords in TOPICS.items():
    mask = df['texto_norm'].apply(lambda t: any(kw in t for kw in keywords))
    count = mask.sum()
    results[topic] = {
        'count': int(count),
        'pct':   round(count / total * 100, 1),
    }

results_sorted = dict(sorted(results.items(), key=lambda x: x[1]['count'], reverse=True))

print('\nTopicos mas mencionados:')
print(f'{"Topico":<35} {"N":>6}  {"Pct":>6}')
print('-' * 52)
for topic, data in results_sorted.items():
    print(f'{topic:<35} {data["count"]:>6}  {data["pct"]:>5.1f}%')

print(f'\nTotal resenas: {total}')
print('\nJSON para HTML:')
for topic, data in results_sorted.items():
    print(f'  "{topic}": {{"count": {data["count"]}, "pct": {data["pct"]}}}')
