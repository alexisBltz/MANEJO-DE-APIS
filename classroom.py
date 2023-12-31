import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = [

"https://www.googleapis.com/auth/classroom.courses.readonly",
"https://www.googleapis.com/auth/drive.metadata.readonly",
"https://www.googleapis.com/auth/classroom.courseworkmaterials",
"https://www.googleapis.com/auth/classroom.topics",
"https://www.googleapis.com/auth/drive.readonly",
"https://www.googleapis.com/auth/classroom.topics.readonly",

]


def main():
    creds = otorgarPermisos()
    idClassrooms = mostrarClassroom(creds)
    print(idClassrooms)
    mi_clase , clase_modelo = idClassrooms
    linksDriveMaterials_SOLUCIONARIOS = linkDriveXsemana(creds, idClassrooms[clase_modelo], 'SOLUCIONARIOS SEMANA 1')
    linksDriveMaterials_SOLUCIONARIOS = linkDriveXsemana(creds, idClassrooms[clase_modelo], 'PRÁCTICAS SEMANA 2')
    prueba = linksDriveMaterials_SOLUCIONARIOS[0]
    nombre = prueba['id']
    pruebaDowload = dowloadMaterials(creds, nombre)
    test = uploadMaterials(creds)
    print(test)
    #subirMaterial(creds, "650438447902", idClassrooms[mi_clase],pruebaDowload)


    #obtener_lista_topics(creds, idClassrooms[mi_clase])
    topics = [
        "650438447902","650443467764","650436816375","646645337765","646645085022","650438232097","650438874831","639270274659","650438418939",
        "650438457213","646644075569","646645343568","650438564658","650438701840","650439967065","646645573715","650439922488",
    ]

def subirMaterial(creds,topics,course_id_aula, materials):
    try:
        service = build('classroom', 'v1', credentials=creds)
        # agregar materiales:
        #for x in range(14):
        """
        tomos = {
            "courseId": course_id_aula,
            "topicId": cursos[x],
            "title": "TOMO 2",
            "description": "",
            "materials": [
                {
                    'link': {
                        'url': urlTomo[x]
                    },
                }
            ],
            "state": "DRAFT",
            "scheduledTime": "2023-11-05T02:30:00Z",
        }
        """
        practicas = {
            "courseId": course_id_aula,
            "topicId": topics[0],
            "title": "PRÁCTICA " + "test",
            "description": "",
            "materials": [
                {
                    'driveFile': {
                        "id": materials,
                    },
                }
            ],
            "state": "DRAFT",
            "scheduledTime": "2023-12-09T02:00:00Z",
        }

        solucionarios = {
            "courseId": course_id_aula,
            "topicId": topics[0],
            "title": "SOLUCIONARIO " + "test",
            "description": "",
            "materials": [
                {
                    'link': {
                        #'url': urlSolucionarios[x]
                    },
                }
            ],
            "state": "DRAFT",
            "scheduledTime": "2023-12-09T15:00:00Z",
        }

        # service.courses().courseWorkMaterials().create(courseId=course_id_aula, body=tomos).execute()
        service.courses().courseWorkMaterials().create(courseId=course_id_aula, body=practicas).execute()
        #service.courses().courseWorkMaterials().create(courseId=course_id_aula, body=solucionarios).execute()




    except HttpError as error:
        print('An error occurred: %s' % error)
def obtener_lista_topics(creds, course_id):
    service = build('classroom', 'v1', credentials=creds)

    # Obtener lista de topics
    topics = service.courses().topics().list(courseId=course_id).execute()

    # Mostrar información de los topics
    if 'topic' in topics:
        lista_topics = topics['topic']
        for topic in lista_topics:
            #print(f"ID del Topic: {topic['topicId']}")
            #print(f"Nombre del Topic: {topic['name']}")
            print(f"\"{topic['topicId']}\",")
    else:
        print("No se encontraron topics en el curso.")

def obtener_idTopic_tema_por_nombre(creds, course_id, nombre_tema):
    service = build('classroom', 'v1', credentials=creds)

    # Obtener la lista de temas del curso
    lista_temas = service.courses().topics().list(courseId=course_id).execute()

    for tema in lista_temas.get('topic', []):
        if tema['name'] == nombre_tema:
            return tema['topicId']

    # Devolver None si no se encuentra el tema
    return None

def linkDriveXsemana(creds, course_id_modelo, nameMaterial):
    info_drive_list = []
    service = build('classroom', 'v1', credentials=creds)

    listaMateriales = service.courses().courseWorkMaterials().list(courseId=course_id_modelo).execute()
    print(listaMateriales)

    for material in listaMateriales['courseWorkMaterial']:
        print(material['title'])
        if material['title']==nameMaterial:
            #print(f"Material de trabajo en el tema con ID: {topic_id}")
            for material_info in material['materials']:
                if 'driveFile' in material_info:
                    drive_file_info = material_info['driveFile']['driveFile']

                    drive_file_id = drive_file_info['id']
                    #pondremos ese :2 para que nos retorne el numero no mas uwu
                    drive_file_title = drive_file_info['title'][:2]
                    info_drive_list.append(
                        {
                            'nombre': drive_file_title,
                            'id': drive_file_id
                        }
                    )
                    #print(info_drive_list)
                else:
                    print("No hay información de Google Drive en este material de trabajo.")


    return info_drive_list

def uploadMaterials(creds, file_id, file_name):

    try:
        # Descargar el contenido del archivo desde Google Drive
        file_content = dowloadMaterials(creds, file_id)

        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": file_name}
        media = MediaFileUpload(io.BytesIO(file_content), mimetype="application/pdf")

        # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')

    except Exception as e:
        print(f"An error occurred: {e}")
        file = None

    return file.get("id") if file else None
def dowloadMaterials(creds, file_id):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.getvalue() if file else None

def drive(creds):
    folder_id = 'MODELOS DE PARTE'
    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(q=f"'{folder_id}' in parents", pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print(f"{item['name']} ({item['id']})")
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


def mostrarClassroom( creds ):

    try:
      service = build("classroom", "v1", credentials=creds)

      # Call the Classroom API
      results = service.courses().list(pageSize=10).execute()
      courses = results.get("courses", [])

      if not courses:
        classroom = {}
      else:
          classroom = {}
          for course in courses:
            classroom.update({course['name']: course['id']})

      return classroom


    except HttpError as error:
      return (f"An error occurred: {error}")


def otorgarPermisos():
    """Shows basic usage of the Classroom API.
      Prints the names of the first 10 courses the user has access to.
      """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
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

    return creds


if __name__ == "__main__":
  main()