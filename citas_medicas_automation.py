from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from datetime import datetime
import time
import winsound
import os

# Configura el navegador
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    # Abre la página web
    driver.get('https://www.citas.med.ec/')
    driver.implicitly_wait(10) 
    
    load_dotenv()
    USUARIO = os.getenv('USUARIO')
    CONTRASENA = os.getenv('CONTRASENA')
    NOMBRE_COMPLETO_PACIENTE = os.getenv('NOMBRE_COMPLETO_PACIENTE')
    MEDICINA_GENERAL = 'MEDICINA GENERAL'
    MEDICINA_FAMILIAR = 'MEDICINA FAMILIAR'
    MENSAJE_NO_DISPONIBILIDAD = "El establecimiento en el que se encuentra adscrito no tiene disponibilidad para el servicio seleccionado. Desea mostrar más establecimientos?"
    INTERVALO_MINUTOS_CONSULTAR = 5
    
    # Login
    driver.find_element(By.ID, "TxtUsuario").send_keys(USUARIO)
    driver.find_element(By.ID, "TxtContrasena").send_keys(CONTRASENA)
    driver.find_element(By.CSS_SELECTOR, '[title="Login"]').click()
    driver.implicitly_wait(10)      
    
    # 1. Agendar una Cita
    agendar = driver.find_element(By.ID, "ContentPlaceHolderPrincipalAgendamientoWeb_imgBtnAgendar")
    agendar.click()    
    driver.implicitly_wait(10)  
    
    # 2. Elejir pariente, se rapido la carga de la pagina, 5s esta bien
    paciente = driver.find_element(By.XPATH, f"//span[contains(text(), '{NOMBRE_COMPLETO_PACIENTE}')]")
    paciente.click()
    # driver.implicitly_wait(10)
    time.sleep(5)
    
    while True:
        
        # 3. Elejir Servicio Medico = "Medicina General", si se demora un poquito, 10s esta bien
        medicina_general_span = driver.find_element(By.XPATH, f"//span[contains(text(), '{MEDICINA_GENERAL}')]")
        medicina_general_span.click()
        # driver.implicitly_wait(10) 
        time.sleep(10)
            
        # 4. Elejir Motivo = "Cita Medica", es rapida la respuesta, 5s esta bien
        cita_medica_a = driver.find_element(By.ID, "ctl00_ContentPlaceHolderPrincipalAgendamientoWeb_WucAgendaCita_RadLstMotivos_ctrl1_LnkBtnMotivo")
        driver.execute_script("arguments[0].scrollIntoView(true);", cita_medica_a)
        # Para darle tiempo a hacer scroll down
        time.sleep(1)
        cita_medica_a.click()    
        # driver.implicitly_wait(5)  
        time.sleep(5)
            
        # Buscar el elemento <p> que contiene "El establecimiento en el que se encuentra adscrito no tiene disponibilidad..."
        mensaje_no_disponibilidad_alert = driver.find_elements(By.XPATH, f"//p[text()='{MENSAJE_NO_DISPONIBILIDAD}']")

        # Verificar si existe
        if len(mensaje_no_disponibilidad_alert) > 0:
            fecha_hora_actual = datetime.now()
            print(f"{fecha_hora_actual}: NO HAY DISPONIBILIDAD EN EL SUBCENTRO ADSCRITO PARA MEDICINA GENERAL")
            cancel_button = driver.find_element(By.CLASS_NAME, "cancel")
            cancel_button.click()
            
            # 3. Elejir Servicio Medico = "Medicina Familiar", si se demora un poquito como en Medicina General, 10s esta bien
            medicina_familiar_span = driver.find_element(By.XPATH, f"//span[contains(text(), '{MEDICINA_FAMILIAR}')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", medicina_familiar_span)
            # Para darle tiempo a hacer scroll up
            time.sleep(1)        
            medicina_familiar_span.click()
            # driver.implicitly_wait(10) 
            time.sleep(10)
            
            
            # 4. Elejir Motivo = "Cita Medica", es rapida la respuesta, 5s esta bien
            cita_medica_a = driver.find_element(By.ID, "ctl00_ContentPlaceHolderPrincipalAgendamientoWeb_WucAgendaCita_RadLstMotivos_ctrl0_LnkBtnMotivo")
            driver.execute_script("arguments[0].scrollIntoView(true);", cita_medica_a)
            # Para darle tiempo a hacer scroll down
            time.sleep(1)
            cita_medica_a.click()    
            # driver.implicitly_wait(10)  
            time.sleep(5)
            
            # Buscar el elemento <p> que contiene "El establecimiento en el que se encuentra adscrito no tiene disponibilidad ..."
            mensaje_no_disponibilidad_alert = driver.find_elements(By.XPATH, f"//p[text()='{MENSAJE_NO_DISPONIBILIDAD}']") 
            if len(mensaje_no_disponibilidad_alert) > 0:
                print(f"{fecha_hora_actual}: NO HAY DISPONIBILIDAD EN EL SUBCENTRO ADSCRITO PARA MEDICINA FAMILIAR")
                cancel_button = driver.find_element(By.CLASS_NAME, "cancel")
                cancel_button.click()            
            else:
                print("SI HAY DISPONIBILIDAD EN EL SUBCENTRO ADSCRITO PARA MEDICINA FAMILIAR")
                winsound.PlaySound('fun_song.wav',winsound.SND_FILENAME)
                print('Fin del programa')
                break
        
        else:
            print("SI HAY DISPONIBILIDAD EN EL SUBCENTRO ADSCRITO PARA MEDICINA GENERAL")
            winsound.PlaySound('fun_song.wav',winsound.SND_FILENAME)
            print('Fin del programa')
            break
        
        print(f"Esperando {INTERVALO_MINUTOS_CONSULTAR} minutos para volver a intentar...")
        time.sleep(INTERVALO_MINUTOS_CONSULTAR*60)

finally:
    driver.quit()
