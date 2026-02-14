from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

PROFILE_DIR = os.path.abspath("./profile")

options = webdriver.ChromeOptions()
options.binary_location = "/snap/bin/chromium"
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")

print("Escanea el QR...")
time.sleep(20)

print("Bot activo")

last_text = ""

while True:
    try:
        chat = driver.find_element(By.XPATH, "//div[@role='textbox']/../../..")
        texto = chat.text

        if texto != last_text:
            last_text = texto
            print("Nuevo cambio detectado")

            if "!ping" in texto.split("\n")[-1]:
                caja = driver.find_element(By.XPATH, "//div[@role='textbox']")
                caja.send_keys("pong")
                caja.send_keys(Keys.ENTER)

    except Exception as e:
        print("Error:", e)

    time.sleep(3)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

PROFILE_DIR = os.path.abspath("./profile")

options = webdriver.ChromeOptions()
options.binary_location = "/snap/bin/chromium"
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")

print("Escanea el QR...")
time.sleep(20)

print("Bot activo")

last_message = ""

while True:
    try:
        mensajes = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")
        
        if mensajes:
            mensaje_actual = mensajes[-1].text

            if mensaje_actual != last_message:
                last_message = mensaje_actual
                print("Mensaje recibido:", mensaje_actual)

                if mensaje_actual == "!ping":
                    caja = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
                    caja.send_keys("pong")
                    caja.send_keys(Keys.ENTER)

    except Exception as e:
        print("Error:", e)

    time.sleep(2)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

PROFILE_DIR = os.path.abspath("./profile")

options = webdriver.ChromeOptions()
options.binary_location = "/snap/bin/chromium"
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")

print("Escanea el QR...")
time.sleep(20)

print("Bot activo")

while True:
    try:
        mensajes = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]")
        if mensajes:
            ultimo = mensajes[-1].text.strip()
            if ultimo == "!ping":
                caja = driver.switch_to.active_element
                caja.send_keys("pong" + Keys.ENTER)
                time.sleep(2)
    except:
        pass

    time.sleep(3)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

PROFILE_DIR = os.path.abspath("./profile")

options = webdriver.ChromeOptions()
options.binary_location = "/snap/bin/chromium"
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")

print("Escanea el QR...")
time.sleep(30)

print("Bot activo")

while True:
    time.sleep(5)
