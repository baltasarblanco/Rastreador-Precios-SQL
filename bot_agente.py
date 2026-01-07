import sqlite3
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# --- CONFIGURACIÓN ---
URL_OBJETIVO = "https://books.toscrape.com" # Web segura para PRACTICAR
DB_NAME = "base_datos_tienda.db"

print ("---🤖 INICIANDO AGENTE DE RASTRO ---")

# 1 .  INVOCAR AL NAVEGADOR
driver = webdriver.Chrome()
driver.get(URL_OBJETIVO)
print (f"✅ Navegando a: {URL_OBJETIVO}")
time.sleep(2) # Esperamos que cargue

# 2 . ENCONTRAR LIBROS
# Buscamos todas las cajitas que tengan la clase "product_pod"
libros = driver.find_elements(By.CLASS_NAME, "product_pod")
print (f"👀 Se encontraron {len(libros)} libros en la portada.")

# 3 . PREPARAR LA CONEXIÓN A LA BASE DE DATOS
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
fecha_hoy = datetime.date.today().isoformat()
contador_guardados = 0

print ("--- 📥 EXTRACCIÓN E INSERCIÓN ---")

# 4 . EL BUCLE MAESTRO
for libro in libros:
    try:
        # Extraer titulo (está dentro de una etiqueta h3 -> a )
        titulo_elemento = libro.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")
        titulo = titulo_elemento.get_attribute("title")

        # Extraer Precio ( esta en la clase "price_color")
        precio_texto = libro.find_element(By.CLASS_NAME, "price_color").text

        # Limpieza de DATOS (Data Cleaning)
        # El precio viene como "£51.77". Python no sabe sumar simbolos raros
        # Quitamos el primer caracter (el £) y convertimos a número
        precio_limpio = float(precio_texto.replace("£",""))

        # INSERTAR EN BASE DE DATOS
        query = "INSERT INTO productos (nombre, precio, fecha) VALUES (?, ?, ?)"
        cursor.execute(query, (titulo, precio_limpio, fecha_hoy))

        contador_guardados += 1
        print (f"💾 Guardado: {titulo} - ${precio_limpio}")

    except Exception as e:
        print (f"❌ Error con un libro: {e}")

# 5 . CERRAR EL CHIRINGUITO
conn.commit()
conn.close()
driver.quit()

print("-" * 30)
print(f"🏆 ÉXITO TOTAL. Se robaron y guardaron {contador_guardados} productos.")

