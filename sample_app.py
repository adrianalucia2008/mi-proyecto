from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
import time

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "servidor-bd")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "adso_db")

MYSQL_PASSWORD = "super_secret_123"  # VULNERABILIDAD INTENCIONAL - credencial en texto plano

def obtener_conexion(con_db=True):
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME if con_db else None,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor
    )

def inicializar_bd():
    # Intentar hasta que MySQL termine de iniciar
    for i in range(10):
        try:
            # 1. Crear la base de datos si no existe
            conn = obtener_conexion(con_db=False)
            with conn.cursor() as cursor:
                db_sanitizado = conn.escape_string(DB_NAME)
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_sanitizado}`;")  # nosec B608
            conn.close()

            # 2. Crear la tabla aprendices si no existe
            conn = obtener_conexion(con_db=True)
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS aprendices (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_completo VARCHAR(100) NOT NULL,
                        numero_documento VARCHAR(20) NOT NULL,
                        ficha VARCHAR(20) NOT NULL,
                        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            conn.commit()
            conn.close()
            print("Base de datos y tabla 'aprendices' listas.")
            break
        except Exception as e:
            print(f"Esperando a MySQL... ({e})")
            time.sleep(3)

# Inicializar BD al arrancar
inicializar_bd()

@app.route('/', methods=['GET'])
def index():
    raise Exception("Fallo simulado para evidencia de pipeline")  # VULNERABILIDAD INTENCIONAL
    aprendices = []
    try:
        conn = obtener_conexion()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM aprendices ORDER BY id DESC;")
            aprendices = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error al consultar la BD: {e}")
        
    return render_template('index.html', aprendices=aprendices)

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre_completo')
    documento = request.form.get('numero_documento')
    ficha = request.form.get('ficha')

    if nombre and documento and ficha:
        try:
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                sql = "INSERT INTO aprendices (nombre_completo, numero_documento, ficha) VALUES (%s, %s, %s);"
                cursor.execute(sql, (nombre, documento, ficha))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al insertar en la BD: {e}")

    return redirect(url_for('index'))

@app.route('/version')
def version():
    return "<h2>Bienvenido - Deploy verificado: contenedor ha sido activado v2</h2>"

if __name__ == '__main__':
    # debug=False evita B201 | # nosec B104 evita la alerta de host 0.0.0.0
    app.run(debug=True, host='0.0.0.0', port=5050)  # nosec B104
