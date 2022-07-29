
import sqlite3
from sqlite3 import Error
import logging

class CountryDB():

    def __init__(self, db_file):
        self.log= logging.getLogger(__name__)
        self.conn=None
        self.db_file=db_file

    def create_connection(self):
        #Crea la conexion a la BD
        self.conn=None
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.log.debug('SQLITE3 CONNECTION CREATED (sqlite v.' + sqlite3.version+')')
        except Error as e:
            self.log.error(e)

    def create_database(self):
        #Crea la tabla en la BD
        try:
            self.drop_table()
            cur=self.conn.cursor()
            sql = 'CREATE TABLE country(region text, contry_name text, language text, time float)'
            cur.execute(sql)
            self.conn.commit()
        except Error as e:
            self.log.error(e)
            self.conn.rollback()

    def drop_table(self):
        #Elimina la tabla en caso de que exista
        try:
            cur=self.conn.cursor()
            cur.execute('DROP TABLE country')
            self.conn.commit()
        except Error as e:
            self.log.debug('DROP is not necessary: [' + str(e)+']')
            self.conn.rollback()

    def add_country(self, row):
        #Agrega una nueva row recibiendo un dict con los datos
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO {tn} (region,contry_name,language,time) VALUES(?, ?, ?, ?)".format(tn='country'),(row['Region'],row['Country Name'],row['Language'],row['Time']))
            self.conn.commit()
        except Error as e:
            self.log.debug(row)
            self.log.error(e)
            self.conn.rollback()
    
    def list_country(self):
        #Regresa una lista de objetos dict con los datos de la tabla sqlite
        try:
            self.conn.row_factory = sqlite3.Row
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM country")
            result = [dict(row) for row in cur.fetchall()]
            return result
        except Error as e:
            self.log.error(e)
            self.conn.rollback()