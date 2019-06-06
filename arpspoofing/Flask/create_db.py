import sqlite3 as sqlite
from werkzeug.security import generate_password_hash
import sys

# Script que crea la base de datos para el ejercicio
# Ejecutar primero

namedb = sys.argv[1]

conn = sqlite.connect(namedb)

print "Abriendo el archivo";

conn.execute('''CREATE TABLE accounts
       (id INT PRIMARY KEY    NOT NULL,
       username       TEXT    NOT NULL,
       account        INT     NOT NULL,
       password       TEXT    NOT NULL,
       balance          REAL);''')

print "Tabla creada"

print "Insercion de datos"

conn.execute('''INSERT INTO account (id, username, email, password, balance)
        VALUES  (1, 'cristian', 345600000, 'qwerty1234', 10000.00); ''')

conn.execute('''INSERT INTO accounts (id, username, account, password, balance)
        VALUES  (2, 'daniel', 3255323322, '1234', 1500.00);''')

conn.execute('''INSERT INTO accounts (id, username, account, password, balance)
        VALUES  (3, 'pepito', 1234567890, 'pepito', 15000.00);''')

conn.execute('''INSERT INTO accounts (id, username, account, password, balance)
        VALUES  (4, 'ebay', 1111100000, 'syper', 0.00);''')

conn.commit()
print "Datos insertados"

print "Cierre de base de datos"
conn.close()
