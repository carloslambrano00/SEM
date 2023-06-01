import pandas as pd
import sys
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# leer el archivo CSV
df = pd.read_csv('ListaSEM.csv')
print(df)
# Copiar DataFrame
df_csv = df.copy(deep=True)

# crear columnas para la URL de búsqueda y la imagen
df['busqueda'] = df['GRUPO_EMPRESARIAL'] + ' Careers'

# Agregar una columna para la URL del portal
# df['url_Portal'] = ''

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# inicializar el driver de Selenium
driver = webdriver.Chrome(options=options)

# para cada fila del DataFrame
for index, row in df.iterrows():
    # obtener la URL de búsqueda
    busqueda = row['busqueda']

    # Hacer una solicitud a la página de resultados de búsqueda de Google
    driver.get('https://www.google.com/search?q=' + busqueda)

    # buscar la URL del portal
    try:
        portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/a')
        url_portal = portal.get_attribute('href')
    except NoSuchElementException:
        try:
            portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/a')
            url_portal = portal.get_attribute('href')
        except NoSuchElementException:
            try:
                portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[1]/div/a')
                url_portal = portal.get_attribute('href')
            except NoSuchElementException:
                try:
                    portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[1]/div/a')
                    url_portal = portal.get_attribute('href')
                except NoSuchElementException:
                    try:
                        portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[2]/div/div/div[1]/div/a')
                        url_portal = portal.get_attribute('href')
                    except NoSuchElementException:
                        try:
                            portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[2]/ul/li/div/div/div/div[1]/div/a')
                            url_portal = portal.get_attribute('href')
                        except NoSuchElementException:
                            try:
                                portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[2]/ul/li/div/div/div/div[1]/div/a')
                                url_portal = portal.get_attribute('href')
                            except NoSuchElementException:
                                try:
                                    portal = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div[1]/div/div/div[1]/div/a')
                                    url_portal = portal.get_attribute('href')
                                except NoSuchElementException as e:
                                    url_portal = None

    time.sleep(4)

    # guardar la URL del portal en el DataFrame
    if url_portal:
        df.at[index, 'url_Portal'] = '<a href="' + url_portal + '">' + df.at[index, 'GRUPO_EMPRESARIAL'] + '</a>'
        print('La dirección es:', url_portal)
    else:
        print('No se encontró la URL de búsqueda para la fila', index + 1)

    if url_portal:
        df_csv.at[index, 'url'] = url_portal

# cerrar el driver de Selenium
driver.quit()

# guardar el DataFrame modificado en un archivo CSV
df_csv.to_csv('ListaSEM_Portal.csv', index=False, columns=df_csv.columns[0:])

# convertir el DataFrame en un archivo HTML
html = df.to_html(escape=False, columns=df.columns[0:])

# escribir el archivo HTML
with open('ListaSEM_Portal.html', 'w') as f:
    f.write(html)