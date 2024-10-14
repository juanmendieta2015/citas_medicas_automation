from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import winsound
import os

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def esperar_elemento(id_elemento, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, id_elemento)))
    
def esperar_elemento_by_XPATH(xpath_elemento, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath_elemento)))    

def login():
    driver.find_element(By.ID, "TxtUsuario").send_keys(USUARIO)
    driver.find_element(By.ID, "TxtContrasena").send_keys(CONTRASENA)
    driver.find_element(By.CSS_SELECTOR, '[title="Login"]').click()
    driver.implicitly_wait(10)     
    
def click_element_by_ID(id, is_scroll_necesary):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id)))
        if is_scroll_necesary:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()  
    except Exception as e:
        print(f"Error al hacer clic en el elemento con ID {id}: {str(e)}")
        
def click_element_by_XPATH(xpath, is_scroll_necesary) :
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))) 
        if is_scroll_necesary:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()  
    except Exception as e:
        print(f"Error al hacer clic en el elemento con XPATH {xpath}: {str(e)}")

def verificar_disponibilidad(mensaje):
    return len(driver.find_elements(By.XPATH, f"//p[text()='{mensaje}']")) > 0

def build_xpath_seleccionar_motivo_link(motivo_cita_medica):
    return f"//fieldset[@id='FieldSet2']//div[contains(., '{motivo_cita_medica}')]//a[contains(text(), 'Seleccionar')]"

def build_xpath_servicio_medico_link(servicio_medico):
    return f"//span[contains(text(), '{servicio_medico}')]"
    
try:
    load_dotenv()
    USUARIO = os.getenv('USUARIO')
    CONTRASENA = os.getenv('CONTRASENA')
    NOMBRE_COMPLETO_PACIENTE = os.getenv('NOMBRE_COMPLETO_PACIENTE')
    SERVICIO_MEDICO = ["MEDICINA GENERAL", "MEDICINA FAMILIAR"]
    MEDICINA_GENERAL = 'MEDICINA GENERAL'
    MEDICINA_FAMILIAR = 'MEDICINA FAMILIAR'
    MOTIVO_CITA_MEDICA = "CITA MEDICA"
    CITAS_MEDICAS_URL = 'https://www.citas.med.ec/'
    MENSAJE_NO_DISPONIBILIDAD = "El establecimiento en el que se encuentra adscrito no tiene disponibilidad para el servicio seleccionado. Desea mostrar más establecimientos?"
    INTERVALO_MINUTOS_CONSULTAR = 0.1
    ICONO_AGENDAR_CITA = "ContentPlaceHolderPrincipalAgendamientoWeb_imgBtnAgendar"
    
    if not USUARIO or not CONTRASENA:
        raise ValueError("Faltan variables de entorno USUARIO o CONTRASENA")
    driver.get(CITAS_MEDICAS_URL)
    driver.implicitly_wait(10) 
    login()
    esperar_elemento(ICONO_AGENDAR_CITA)
    click_element_by_ID(ICONO_AGENDAR_CITA, False)
    
    nombre_paciente = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{NOMBRE_COMPLETO_PACIENTE}')]"))
    )
    nombre_paciente.click()
    time.sleep(5)
     
    while True:
        fecha_hora_actual = datetime.now().strftime("%H:%M:%S")
        if 'MEDICINA GENERAL' in SERVICIO_MEDICO:
            # Click en Medicina General
            xpath_medicina_general_link = build_xpath_servicio_medico_link(MEDICINA_GENERAL)
            esperar_elemento_by_XPATH(xpath_medicina_general_link)
            click_element_by_XPATH(xpath_medicina_general_link, False)
            time.sleep(3)
        
            # Click en "Seleccionar" de Citas Médicas de Medicina General
            xpath_seleccionar_cita_medica_link = build_xpath_seleccionar_motivo_link(MOTIVO_CITA_MEDICA)
            esperar_elemento_by_XPATH(xpath_seleccionar_cita_medica_link)
            click_element_by_XPATH(xpath_seleccionar_cita_medica_link, True)
            
            # Verificar disponibilidad de cita medica
            if verificar_disponibilidad(MENSAJE_NO_DISPONIBILIDAD) > 0:
                # No hay disponibilidad
                print(f"{fecha_hora_actual}: NO hay disponibilidad en el subcentro adscrito para Medicina General")
                cancel_button = driver.find_element(By.CLASS_NAME, "cancel")
                cancel_button.click()
            else:
                # Si hay disponibilidad
                print("SÍ hay disponibilidad en el subcentro adscrito para Medicina General")
                winsound.PlaySound('fun_song.wav',winsound.SND_FILENAME)
                print('Fin del programa')
                break

        if 'MEDICINA FAMILIAR' in SERVICIO_MEDICO:
            # Click en Medicina Familiar
            xpath_servicio_medico_link = build_xpath_servicio_medico_link(MEDICINA_FAMILIAR)
            esperar_elemento_by_XPATH(xpath_servicio_medico_link)
            click_element_by_XPATH(xpath_servicio_medico_link, False)
            time.sleep(3)                    
            
            # Click en "Seleccionar" de Citas Médicas de Medicina Familiar
            xpath_seleccionar_cita_medica_link = build_xpath_seleccionar_motivo_link(MOTIVO_CITA_MEDICA)
            esperar_elemento_by_XPATH(xpath_seleccionar_cita_medica_link)
            click_element_by_XPATH(xpath_seleccionar_cita_medica_link, True)            

            # Verificar disponibilidad de cita medica
            if verificar_disponibilidad(MENSAJE_NO_DISPONIBILIDAD) > 0:
                # No hay disponibilidad
                print(f"{fecha_hora_actual}: NO hay disponibilidad en el subcentro adscrito para Medicina Familiar")
                cancel_button = driver.find_element(By.CLASS_NAME, "cancel")
                cancel_button.click()     
            else:
                # Si hay disponibilidad
                print("SÍ hay disponibilidad en el subcentro adscrito para Medicina Familiar")
                winsound.PlaySound('fun_song.wav',winsound.SND_FILENAME)
                print('Fin del programa')
                break        
        
        print(f"Esperando {INTERVALO_MINUTOS_CONSULTAR} minutos para volver a intentar...")
        time.sleep(INTERVALO_MINUTOS_CONSULTAR*60)
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    driver.quit()