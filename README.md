# Prueba Técnica Tangelo Fintech

El objetivo de esta prueba es desarrollar una aplicación python que genere la siguiente tabla:

| Region | Country Name | Language | Time
| ------------- | ------------- | ------------- |------------- |
| Africa  | Angola | AF4F4762F9BD3FOF4A10CAF5B6E63DC4CE543724 | 0.23ms |
| | | | |
| | | | |
| | | | |

Tomando en cuenta las siguientes consideraciones:

- De https://restcountries.com/ obtenga el nombre del idioma que habla el país y encriptelo con SHA1 

- En la columna Time ponga el tiempo que tardó en armar la fila (debe ser automático)

- La tabla debe ser creada en un DataFrame con la librería PANDAS 

- Con funciones de la librería pandas muestre el tiempo total, el tiempo promedio, el tiempo mínimo y el máximo que tardo en procesar todas las filas de la tabla

- Guarde el resultado en sqlite

- Genere un Json de la tabla creada y guárdelo como data.json


## Diseño

El sistema se dividirá en 4 secciones:

### Obtener información de los paises

Para esta sección se hara un request GET a la siguiente URL: https://restcountries.com/v2/all?fields=name,region,languages

Nota importante: agregando el parametro 'fields' a la URL se pueden obtener solamente los campos que necesitamos.

Teniendo una respuesta como la siguiente:

```
[
    {
        "name": "Afghanistan",
        "region": "Asia",
        "languages": [
            {
                "iso639_1": "ps",
                "iso639_2": "pus",
                "name": "Pashto",
                "nativeName": "پښتو"
            },
            {
                "iso639_1": "uz",
                "iso639_2": "uzb",
                "name": "Uzbek",
                "nativeName": "Oʻzbek"
            },
            {
                "iso639_1": "tk",
                "iso639_2": "tuk",
                "name": "Turkmen",
                "nativeName": "Türkmen"
            }
        ],
        "independent": false
    },
    {
        "name": "Åland Islands",
        "region": "Europe",
        "languages": [
            {
                "iso639_1": "sv",
                "iso639_2": "swe",
                "name": "Swedish",
                "nativeName": "svenska"
            }
        ],
        "independent": false
    },
    {
        "name": "Albania",
        "region": "Europe",
        "languages": [
            {
                "iso639_1": "sq",
                "iso639_2": "sqi",
                "name": "Albanian",
                "nativeName": "Shqip"
            }
        ],
        "independent": false
    },
    {
        "name": "Algeria",
        "region": "Africa",
        "languages": [
            {
                "iso639_1": "ar",
                "iso639_2": "ara",
                "name": "Arabic",
                "nativeName": "العربية"
            }
        ],
        "independent": false
    }]
```

### Generar DataFrame

En esta sección se utiliza la libreria pandas para crear un DataFrame que contendra la tabla a generar. Por cada fila se deberan de realizar los siguientes procesos:

1. Tomar el tiempo al inicio y al final de procesar la fila para calcular la columna Time.
2. Tomar un solo lenguaje de la lista en caso de que el pais contenga mas de uno.
3. Encriptar el lenguaje en SHA1.
4. Almacenar la misma fila en la tabla de sqlite.



### Calcular Tiempos
En esta sección utilizaremos las funciones sum, mean, min y max en la columna 'Time' del datarow para obtener los calculos necesarios.

De la siguiente manera:
```
total_time = df['Time'].sum()
mean_time = df['Time'].mean()
min_time = df['Time'].min()
max_time = df['Time'].max()
```

### Exportar JSON
En esta sección haremos un select en la tabla de sqlite y lo exportaremos a un archivo json.


## Arquitectura

* db
    * __init__.py
    * CountryDB.py (Clase con los metodos para la BD de sqlite)
* app_config.json  (Archivo de configuración de la aplicacion, como logs y archivos)
* Tangelo_Fintech.py (Clase main de la aplicacion con todos los metodos prinicipales)

## Requerimientos

* Python 3.7
* pip3 libs:
    * certifi==2022.6.15
    * charset-normalizer==2.1.0
    * idna==3.3
    * numpy==1.21.6
    * pandas==1.3.5
    * python-dateutil==2.8.2
    * pytz==2022.1
    * requests==2.28.1
    * six==1.16.0
    * urllib3==1.26.11

Todas las librerias se encuentran en el archivo requirements.txt


## Instalación

1. Crear un Virtual Environment (En caso de no estar creado)
```
python3 -m venv .venv
```
2. Activar el Environment
```
source .venv/bin/activate
```
3. Instalar requirements
```
pip3 install -r requirements.txt
```
## Usage

1. Activar el Environment
```
source .venv/bin/activate
```
1. Run Tangelo_Fintech class
```
python Tangelo_Fintech.py
```


