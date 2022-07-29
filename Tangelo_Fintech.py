
import requests
import logging, logging.handlers
import os
import json
import pandas as pd
import hashlib
import time
from db import CountryDB

class Tangelo_Fintech():

    def __init__(self, rootPath, config_file):
        self.app_config = self.loadConfig(config_file,rootPath)
        self.logHelper()
        self.log = logging.getLogger(__name__)
        self.country_db = CountryDB(self.app_config['DB_FILE'])
        self.country_db.create_connection()
        self.country_db.create_database()
        
    def loadConfig(self,config_file_name,rootPath):
        f = open(os.path.join(rootPath, config_file_name))
        cfg = json.load(f)
        f.close()
        return cfg

    def logHelper(self):
        loggingSection=self.app_config['logging']
        DEFAULT_LOG_FORMATTER = loggingSection['DEFAULT_LOG_FORMATTER']
        DEFAULT_LOG_LEVEL = loggingSection['DEFAULT_LOG_LEVEL']
        logging.basicConfig(format=DEFAULT_LOG_FORMATTER, level=DEFAULT_LOG_LEVEL)
        logging.getLogger(__name__).debug('Logging initialized...')

    def getCountriesData(self):
        #Realiza el request REST para obtener la informacion de los paises
        self.log.debug('In [getCountriesData]')
        try:
            r = requests.get(self.app_config['REST_URL'])
            if r.status_code == 200:
                body_response = r.json()
                return body_response
            else:
                self.log.error('REST Services response ['+str(r.status_code)+']')
        except Exception as e:
            self.log.error(e)

    def generateDataFrame(self, rest_data):
        #recibe la lista de los paises y genera el DataFrame
        self.log.debug('In [generateDataFrame]')
        start = time.time()
        data = rest_data[0]
        lang = data['languages']
        language_name = lang[0]['name']
        row = {}
        row['Region'] = data['region']
        row['Country Name'] = data['name']
        row['Language'] = str(self.sha1encode(str(language_name).encode()))
        #row['Language'] = str(language_name)
        end = time.time()
        row['Time'] = (end - start)

        df = pd.DataFrame(row, index=[0])
        self.country_db.add_country(row)

        self.log.info('Total countries: '+str(len(rest_data)))

        for country in rest_data[1:len(rest_data)]:
            start = time.time()
            lang = country['languages']
            language_name = lang[0]['name']
            row = {}
            row['Region'] = country['region']
            row['Country Name'] = country['name']
            row['Language'] = str(self.sha1encode(str(language_name).encode()))
            #row['Language'] = str(language_name)
            end = time.time()
            row['Time'] = (end - start)
            df = df.append(row, ignore_index = True)
            self.country_db.add_country(row)
        
        return df

    def sha1encode(self, data):
        #Realiza el encriptado de la informacion en SHA1
        h = hashlib.new("sha1", data)
        hexData = h.hexdigest()
        self.log.debug(str(data) + ' encrypted to ' + str(hexData))
        return hexData

    def calculateTimes(self, df):
        #Calcula los tiempos de la tabla DataFrame de pandas
        total_time = df['Time'].sum()
        mean_time = df['Time'].mean()
        min_time = df['Time'].min()
        max_time = df['Time'].max()
        self.log.info('Total Time: '+ str(total_time) + ' seg')
        self.log.info('Mean Time: '+ str(mean_time) + ' seg')
        self.log.info('Min Time: '+ str(min_time) + ' seg')
        self.log.info('Max Time: '+ str(max_time) + ' seg')

    def exportJson(self):
        #genera el archivo json
        data = self.country_db.list_country()
        with open(self.app_config['JSON_FILE'], 'w') as f:
            json.dump(data, f, indent=2)

    
if __name__ == '__main__':
    rootPath=os.path.dirname(__file__)
    config_file="app_config.json"
    app = Tangelo_Fintech(rootPath,config_file)
    data = app.getCountriesData()
    df = app.generateDataFrame(data)
    app.calculateTimes(df)
    app.exportJson()
    
    