import pymysql

def _get_connection():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database= 'Greeneery')
        return connection
    except:
        print("Error connecting to the database")
        return None
