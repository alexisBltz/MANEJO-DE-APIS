#import pyautogui
from PIL import Image
#import pygetwindow as gw
import mss
#import pyautogui as pg
import datetime
import time
from plyer import notification
#import webbrowser as web

import pyperclip

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

"""import pygetwindow as gw
from PIL import ImageGrab
from google.oauth2 import service_account"""

#CAMBIA TODOS LOS DIAS EL ID DE TU PARTEEEEEEEEEEEEEEEE

sheetToday = "1XJ70lOnOg6zNEnG-Y1PfThAoosdYCrU84kEe0TwF6W8"

# PANTALLA DE LA LAPTOP

"""
def enviarReportes(indice, estado):
    #PARA QUE SE MANDEN LOS REPORTES POR WHATSAPP
    web.open('https://web.whatsapp.com/')
    time.sleep(10)
    pg.click(409,367)
    time.sleep(4)
    pg.click(1230,965)
    pyautogui.typewrite("AULA: 104-I")
    pyautogui.hotkey('shift','enter')

    profesor, curso= compararDia(indice)

    pyautogui.typewrite("DOCENTE: "+ profesor)
    pyautogui.hotkey('shift', 'enter')

    pyautogui.typewrite("CURSO: "+ curso)
    pyautogui.hotkey('shift', 'enter')

    pyautogui.typewrite("REPORTE: DOCENTE "+estado)
    pyautogui.press('enter')
    time.sleep(2)
    pg.hotkey('ctrl','w')
    time.sleep(1)
"""
cursos_info = {
    1: ("PERCY CHOQUE", "BIOLOGIA"),
    2: ("HOLGER NIETO", "CIVICA"),
    3: ("JOSE VALDIVIA", "FILOSOFIA"),
    4: ("VIRGINIA SOTO", "FISICA"),
    5: ("JESUS CACERES", "GEOGRAFIA"),
    6: ("JOSE PAREDES", "HISTORIA"),
    7: ("NILDE LAURO", "INGLES"),
    8: ("GABRIELA AYMER", "LENGUAJE"),
    9: ("JOSE MESTAS", "LITERATURA"),
    10: ("FREDY GAMARRA", "MATEMATICA"),
    11: ("ROCIO VILCA", "PSICOLOGIA"),
    12: ("GLISETH MOYA", "QUIMICA"),
    13: ("BRUNO LUQUE", "RAZ MATEMATICO"),
    14: ("YAHAIRA GUTIERREZ", "RAZ VERBAL"),
}
def compararDia(indice):
    fecha = datetime.datetime.now()
    diaHoy = fecha.weekday()

    dias_clases = {
        0: [1, 4, 12, 13, 14, 10],  # lunes
        1: [8, 4, 12, 13, 14, 10],  # martes
        2: [1, 4, 12, 13, 14, 10],  # miércoles
        3: [8, 9, 3, 5, 6, 10],     # jueves
        4: [1, 4, 12, 13, 14, 10],  # viernes
        5: [8, 9, 2, 5, 7, 11],     # sábado
    }

    if diaHoy in dias_clases:
        cursos = dias_clases[diaHoy]
        try:
            profesor, curso = cursos_info[cursos[indice]]
            return profesor, curso
        except IndexError:
            return "No hay clases para este índice."
    else:
        return "Hoy no hay clases."
def copiarPortapapeles( indice, estado = None ):

    if indice == 23:
        reporte = "✍ AULA: 104-1 ️✍ \n📌PARTE DOCENTE SUBIDO \n📌GRABACION FINALIZADA\n📌REGISTRO DE TEMAS LLENADO \n📌ASISTENCIA REGISTRADA \n📌ENLACE OCULTO \n📌GRABACIONES SUBIDAS"
        notification_message = "REPORTE FINAL COPIADO CON EXITO"
    elif indice == 7 or indice == 15:
        reporte = "✍ AULA: 104-1 ️✍ \n📌GRABACION FINALIZADA \n📌ASISTENCIA REGISTRADA \n📌CAMARA APAGADA"
        notification_message = "REPORTE DE DESCANSO COPIADO CON EXITO"
    else:
        profesor, curso = compararDia(indice)
        reporte = f"✍ *AULA: 104-1* ️✍\n📌*CURSO:* {curso}\n📌*DOCENTE:* {profesor}\n📌*REPORTE:* DOCENTE {estado}"
        notification_message = "REPORTE TOMADO CON EXITO"

    pyperclip.copy(reporte)
    reportePegado = pyperclip.paste()
    notification.notify(
        title="UWU",
        message=notification_message,
    )

    return reportePegado


def tomarCaptura(id):

    with mss.mss() as mss_instance:
        monitor = mss_instance.monitors[2]
        screenshot = mss_instance.grab(monitor)

        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
        name = "c"+str(id)+"-"+str(datetime.datetime.now().strftime(("%m%d-%H%M")))+".png"
        print(name)
        ruta_guardado= "D:\CEPRE\caps"
        ruta_completa =  ruta_guardado + "/" + name

        img.save(ruta_completa, 'PNG')
        """notification.notify(
            title="UWU",
            message="Captura tomada con exito",
        )"""

        return name


def comparar_hora(hora_objetivo):

    while True:
        ahora = datetime.datetime.now().time()
        if ahora.hour == hora_objetivo.hour and ahora.minute == hora_objetivo.minute and ahora.second == hora_objetivo.second:
            break
        time.sleep(1)


def main():

    horas_objetivos = [

        datetime.time(7, 00, 0), #0
        datetime.time(7, 40, 0), #1
        datetime.time(7, 45, 0),
        datetime.time(8, 25, 0),
        datetime.time(8, 30, 0), #4
        datetime.time(9, 10, 0), #5
        datetime.time(9, 15, 0),
        datetime.time(9, 55, 0), #descanso 7

        datetime.time(10, 45, 0), #8
        datetime.time(11, 25, 0), #9
        datetime.time(11, 30, 0),
        datetime.time(12, 10, 0),
        datetime.time(12, 15, 0), #12
        datetime.time(12, 55, 0), #13
        datetime.time(13, 00, 0),
        datetime.time(13, 40, 0), #descanso 15

        datetime.time(14, 30, 0), #16
        datetime.time(15, 10, 0), #17
        datetime.time(15, 15, 0),
        datetime.time(15, 55, 0),
        datetime.time(16, 00, 0), #20
        datetime.time(16, 40, 0), #21
        datetime.time(16, 45, 0),
        datetime.time(17, 25, 0), # reporte final 23

    ]
    i = 0
    hora_actual = datetime.datetime.now()
    for hora in horas_objetivos:
        if hora_actual.hour>hora.hour or (hora_actual.hour == hora.hour and hora_actual.minute>hora.minute):
            print("cambiando hora")
            i = i + 1
            continue
        else:
            comparar_hora(hora) #compara horas

            print(i)
            if i == 7 or i == 15:
                copiarPortapapeles(i)
                putCapSheets(tomarCaptura(i), i, 'N')
                i = i + 1
            elif i == 23:
                copiarPortapapeles(i)
                putCapSheets(tomarCaptura(i), i, 'N')
                i = i + 1
            else:
                if i % 2 == 0:
                    indice = int(i / 4)
                    copiarPortapapeles(indice, "PUNTUAL")
                    putCapSheets(tomarCaptura(i), int(i/2), 'M')
                    i = i + 1
                else:
                    indice = int((i - 1) / 4)
                    copiarPortapapeles(indice, "CONTINUA")
                    putCapSheets(tomarCaptura(i), int(i/2), 'N')
                    i = i + 1

            """"
            time.sleep(2)
            if i % 2 == 0:
                indice = int (i/2)
                enviarReportes(indice, "PUNTUAL")
            else:
                enviarReportes(indice, "CONTINUA")
            i=i+1
            """

def putCapSheets(name, fila, columna):

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly",
              "https://www.googleapis.com/auth/drive",
              "https://www.googleapis.com/auth/spreadsheets",
              ]
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:

        service = build("sheets", "v4", credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        #Subir Materiaaal
        file_metadata = {
            'name': name,
            'parents': ['1BTJ-hSwD38mvl6THXuKuBGFwYqwDiwne'],  # ID de la carpeta de Google Drive donde se almacenará la imagen
        }
        filename= "D:\\CEPRE\\caps\\" + name
        media = MediaFileUpload(filename, mimetype='image/png')
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Obtener el enlace compartido público de la imagen
        file_id = uploaded_file['id']
        permissions = drive_service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()

        """
        response = drive_service.files().list(q=f"'{'1BTJ-hSwD38mvl6THXuKuBGFwYqwDiwne'}' in parents and mimeType='image/png'",
                                               fields="files(id)").execute()
        files = response.get('files')
        """

        image_url = f'https://drive.google.com/uc?id={file_id}'


        # Itera sobre cada imagen y la inserta en la hoja de cálculo

        cell_reference = 'PARTE!' + columna + str(fila+11)
        formula = '=IMAGE(\"' + image_url + '\")'
        cell_body = {'range': f'{cell_reference}', 'values': [[formula]]}

        #ACA CAMBIA EL SHEET CADA DIA

        service.spreadsheets().values().update(spreadsheetId=sheetToday, body=cell_body,
                                                       range=f'{cell_reference}', valueInputOption='RAW').execute()
        print("IMAGEN SUBIDA")



    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()