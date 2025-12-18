import requests
import pandas as pd

datos_de_todas_las_ciudades = pd.DataFrame()

ciudades_y_código = {
    "Bilbao": "1082",    
    "Vitoria": "9091R",
    "Donostia": "1024E",
    "Valencia": "8414A",
    "Málaga": "6172X",
    "Granada": "5530E",
    "Cordoba": "5402",
    "Pamplona": "9262",
    "Madrid": "3129"
}

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cmtvLnp1Z2F6YWdhQGFsdW1uaS5tb25kcmFnb24uZWR1IiwianRpIjoiZWFmOGZlMTEtODFjMC00OGM4LTlmZDQtMWM2NjllNmFkYjdjIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NjQxNzA3MDgsInVzZXJJZCI6ImVhZjhmZTExLTgxYzAtNDhjOC05ZmQ0LTFjNjY5ZTZhZGI3YyIsInJvbGUiOiIifQ.F1wtqN1qRQiLzDyk2IVBK9d8B941SKWec6CoqTzOqKw"

for ciudad, indicativo in ciudades_y_código.items():
  url = ("https://opendata.aemet.es/opendata/api/" +
        "valores/climatologicos/diarios/datos/" +
        "fechaini/2022-01-01T00:00:00UTC/fechafin" +
        f"/2022-01-31T23:59:59UTC/estacion/{indicativo}/")

  respuesta = requests.get(
      url,
      params={'api_key': API_KEY},
      headers={'cache-control': 'no-cache'}
  )

  respuesta_json = respuesta.json()

  if respuesta_json['descripcion'] == 'exito':
      url_de_los_datos = respuesta_json['datos']

      datos_de_esta_ciudad = pd.read_json(url_de_los_datos, encoding='latin/1')

      datos_de_esta_ciudad['prec'] = datos_de_esta_ciudad['prec'].replace('Ip', '0')

      datos_de_esta_ciudad['ciudad'] = ciudad

      datos_de_todas_las_ciudades = pd.concat([
          datos_de_todas_las_ciudades, datos_de_esta_ciudad
      ])
  else:
      print("Error en ciudad:", ciudad, "->", respuesta_json['descripcion'])