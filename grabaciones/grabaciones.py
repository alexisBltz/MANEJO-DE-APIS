import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from datetime import datetime
import locale


SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]


def authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def move_and_rename_files(service, folder_id_origen, folder_id_destino, nuevo_prefijo):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')

        response = service.files().list(
            q=f"'{folder_id_origen}' in parents and mimeType='video/mp4'",
            fields="files(id, name, createdTime)"
        ).execute()
        files = response.get('files', [])



        i=0

        for file in files:
            hora_video = file['name'][25:27]
            print(file)
            fecha_video = file['name'][22:24] + "/" + file['name'][19:21] + "/" + file['name'][14:18]
            print(fecha_video)
            fecha_indicada = datetime.strptime(fecha_video, '%d/%m/%Y')
            nombre_dia = fecha_indicada.strftime("%A").encode('latin-1').decode('utf-8').upper()

            nameSubcarpeta = fecha_indicada.strftime(f'{nombre_dia} %d/%m/%Y')

            print(nameSubcarpeta)

            if hora_video == '06':
                numero = "(PRIMERA GRABACIÓN)"
            elif hora_video == '10':
                numero = '(SEGUNDA GRABACIÓN)'
            else:
                numero = '(TERCERA GRABACIÓN)'

            archivo_id = file['id']

            nuevo_nombre = f"{nameSubcarpeta} {numero}"

            # Actualizar el nombre del archivo
            service.files().update(fileId=archivo_id, body={'name': nuevo_nombre}).execute()

            # Mover el archivo a la subcarpeta correspondiente al día de la semana
            subcarpeta_destino = nameSubcarpeta

            #CREA O VERIFICA QUE EXISTE:
            subcarpeta_destino_id = obtener_id_subcarpeta(service, folder_id_destino, subcarpeta_destino)

            if subcarpeta_destino_id:
                # Agregar la subcarpeta de destino a los padres del archivo
                service.files().update(
                    fileId=archivo_id,
                    addParents=subcarpeta_destino_id,
                    removeParents=folder_id_origen
                ).execute()
                print(
                    f"Archivo '{file['name']}' movido y renombrado como '{nuevo_nombre}' a la subcarpeta destino."
                )

            i= i+1

    except HttpError as error:
        print(f"An error occurred: {error}")


#CREARA LA CARPETA CON LA FECHA ESTABLECIDA:
def obtener_id_subcarpeta(service, carpeta_padre_id, nombre_subcarpeta):
    # EL NOMBRE DE LA CARPETA_PADRE_ID ES LA SEMANA BUSCA LA SUBCARPETA


    response = service.files().list(
        q=f"'{carpeta_padre_id}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    subcarpetas = response.get('files', [])

    # Buscar la subcarpeta con el nombre deseado
    for subcarpeta in subcarpetas:
        if subcarpeta['name'] == nombre_subcarpeta:
            return subcarpeta['id']

    # Si la subcarpeta no existe, crearla y devolver su ID
    nueva_subcarpeta = service.files().create(
        body={'name': nombre_subcarpeta, 'parents': [carpeta_padre_id], 'mimeType': 'application/vnd.google-apps.folder'}
    ).execute()

    return nueva_subcarpeta['id']

def main():
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

    creds = authenticate()

    try:
        service = build("drive", "v3", credentials=creds)

        folder_id_origen = '1NVp0MfPWLWTX3KwraZ9JB8HZzmmPF8T0'


        #CAMBIA CADA QUE SE CAMBIE DE SEMANAAAAAAAAAAAAAAAAAAAAAAAA
        folder_id_destino = '1xqFqS9tdUrs13qjWyzfZUw0-xqr7bTzy'
        nuevo_prefijo = 'nuevo_prefijo'

        move_and_rename_files(service, folder_id_origen, folder_id_destino, nuevo_prefijo)

    except HttpError as error:
        print(f"An error occurred: {error}")



if __name__ == "__main__":
    main()