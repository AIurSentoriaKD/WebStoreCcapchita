#libreria utilizada para la BD
import pyodbc
conn = None
#metodo llamado en la clase principal para realizar la conexión con la variable global 'conn'
def init():
    server = 'DESKTOP-F5IOQT8,1433' 
    database = 'DBCcaphita' 
    username = 'sqlUsuario' 
    password = '123456789' 
    global conn
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

