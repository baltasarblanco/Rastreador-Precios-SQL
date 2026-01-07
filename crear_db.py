import sqlite3

print ("--- 🏗️ INICIANDO SISTEMA SQL ---")

# 1 . Conexión ( Abrir la puerta )
# Si el archivo no existe, Python lo crea automáticamente.
conn = sqlite3.connect("base_datos_tienda.db")
print("✅ Base de datos conectada/creada.")

# 2. EL CURSOR (El brazo robótico)
# Es el encargado de ejecutar las órdenes dentro de la base.
cursor = conn.cursor()

# 3. CREAR TABLA (Si no existe)
# SQL es un lenguaje propio. Aquí escribimos en SQL dentro de Python.
# Vamos a guardar: nombre, precio y fecha.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL,
        fecha TEXT
    )
''')

print ("✅ Tabla 'productos' verificada.")

# 4 .  GUARDAR CAMBIOS (commit)
# ¡CRUCIAL! Si no haces commit, nada se guarda.
conn.commit()

# 5 . CERRAR !
conn.close()
print ("👋 Conexión cerrada.")
