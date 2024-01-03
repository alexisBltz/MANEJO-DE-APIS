import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload


# permisos
SCOPES = [

"https://www.googleapis.com/auth/classroom.courses.readonly",
"https://www.googleapis.com/auth/drive.metadata.readonly",
"https://www.googleapis.com/auth/classroom.courseworkmaterials",
"https://www.googleapis.com/auth/classroom.topics",
"https://www.googleapis.com/auth/drive.readonly",
"https://www.googleapis.com/auth/classroom.topics.readonly",
"https://www.googleapis.com/auth/drive.file",

]


def main():
    #otorgamos permisos
    creds = otorgarPermisos()

    #sacamos ids de ambos classrooms
    idClassrooms = mostrarClassroom(creds)

    #pones las partes del diccionario en dos variables
    mi_clase , clase_modelo = idClassrooms

    obtener_lista_topics(creds, idClassrooms[mi_clase])

    topics = [
        "646645337765",
        "646645085022",
        "650438232097",
        "650438874831",
        "639270274659",
        "650438418939",
        "650438457213",
        "646644075569",
        "646645343568",
        "650438564658",
        "650438701840",
        "650439967065",
        "646645573715",
        "650439922488",
    ]


    # NUmero de semana que estamos
    n=2
    # Sacamos los links de las practicas y solucionarios respectivos
    linksDriveMaterials_SOLUCIONARIOS = linkDriveXsemana(creds, idClassrooms[clase_modelo], 'SOLUCIONARIOS SEMANA '+str(n-1))
    linksDriveMaterials_PRACTICAS = linkDriveXsemana(creds, idClassrooms[clase_modelo], 'PRÁCTICAS SEMANA '+str(n))
    linksDriveMaterials_TOMOS = linkDriveXsemana(creds, idClassrooms[clase_modelo], 'TOMOS 1')
    for x in range(14):
        # Sacamos los datos de la lista de diccionarios
        linkDriveSol = linksDriveMaterials_SOLUCIONARIOS[x]
        linkDrivePrac = linksDriveMaterials_PRACTICAS[x]
        #linkDriveTom = linksDriveMaterials_TOMOS[0]
        nameS, idS = linkDriveSol
        nameP, idP = linkDrivePrac

        #PARA TOMOS
        #nameT, idT = linkDriveTom

        """
        print(linkDriveSol[nameS]+"---"+linkDriveSol[idS])
        print("---"*10)
        print(linkDrivePrac[nameP] + "---" + linkDriveSol[idP])
        """

        # Vemos el id del curso al que pertenece

        topicS = topics[linkDriveSol[nameS]]

        """
        print(linkDriveSol[nameS])
        print("topic: "+ topicS)
        """

        topicP = topics[linkDrivePrac[nameP]]

        """
        print(linkDrivePrac[nameP])
        print("topic: " + topicP)
        """

        # PARA TOMOS
        #topicT= topics[linkDrivePrac[nameT]]


        # Sacamos el id una vez subido a nuestro a nuestro google drive

        # Sol
        Smaterialsbytes = dowloadMaterials(creds, linkDriveSol[idS])

        idDriveMaterialUploadS = uploadMaterials(creds, Smaterialsbytes, "test")

        subirMaterial(creds, topicS, idClassrooms[mi_clase], idDriveMaterialUploadS, "S")


        # Prac
        Pmaterialsbytes = dowloadMaterials(creds, linkDrivePrac[idP])

        idDriveMaterialUploadP = uploadMaterials(creds, Pmaterialsbytes, "test")

        subirMaterial(creds, topicP, idClassrooms[mi_clase], idDriveMaterialUploadP, "P")


        """
        #PARA TOMOS
        Tmaterialsbytes = dowloadMaterials(creds, linkDrivePrac[idT])
    
        idDriveMaterialUploadT = uploadMaterials(creds, Tmaterialsbytes, "test")
    
        subirMaterial(creds, topicT, idClassrooms[mi_clase], idDriveMaterialUploadT, "P")
        
        """




def subirMaterial(creds, topic, course_id, materials, identificador):
    try:
        print(materials)
        service = build('classroom', 'v1', credentials=creds)
        # agregar materiales:
        #for x in range(14):

        if identificador=="T":
            tomos = {
                "courseId": course_id,
                "topicId": topic,
                "title": "TOMO 2",
                "description": "",
                "materials": [
                    {
                        'driveFile': {
                            'driveFile': {
                                "title": "test",
                                "id": materials,
                            },
                            "shareMode": "VIEW"
                        },

                    }
                ],
                "state": "DRAFT",
                "scheduledTime": "2023-11-05T02:30:00Z",
            }
            service.courses().courseWorkMaterials().create(courseId=course_id, body=tomos).execute()
        elif identificador=="P":
            practicas = {
                "courseId": course_id,
                "topicId": topic,
                "title": "PRÁCTICA " + "test",
                "description": "",
                "materials": [
                    {
                        'driveFile': {
                            'driveFile': {
                                "title": "test",
                                "id": materials,
                            },
                            "shareMode": "VIEW"
                        },

                    }
                ],
                "state": "DRAFT",
                #"scheduledTime": "2023-12-09T02:00:00Z",
            }
            service.courses().courseWorkMaterials().create(courseId=course_id, body=practicas).execute()
        else:
            solucionarios = {
                "courseId": course_id,
                "topicId": topic,
                "title": "SOLUCIONARIO test",
                "description": "",
                "materials": [
                    {
                        'driveFile': {
                            'driveFile': {
                                "title": "test",
                                "id": materials,
                            },
                            "shareMode": "VIEW"
                        },

                    }
                ],
                "state": "DRAFT",
                #"scheduledTime": "2023-12-09T15:00:00Z",
            }
            service.courses().courseWorkMaterials().create(courseId=course_id, body=solucionarios).execute()
            print("Material Subido")


    except HttpError as error:
        print(f'An error occurredddd: {error.response}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
def obtener_lista_topics(creds, course_id):
    service = build('classroom', 'v1', credentials=creds)

    # Obtener lista de topics
    topics = service.courses().topics().list(courseId=course_id).execute()

    # Mostrar información de los topics
    if 'topic' in topics:
        lista_topics = topics['topic']
        for topic in lista_topics:

            print(f"Nombre del Topic: {topic['name']}")
            print(f"ID del Topic: {topic['topicId']}")
            print("----"*10)
            #print(f"\"{topic['topicId']}\",")
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
    #print(listaMateriales)

    for material in listaMateriales['courseWorkMaterial']:
        if material['title'] == nameMaterial:
            #print(f"Material de trabajo en el tema con ID: {topic_id}")
            for material_info in material['materials']:
                if 'driveFile' in material_info:
                    drive_file_info = material_info['driveFile']['driveFile']

                    drive_file_id = drive_file_info['id']
                    #pondremos ese :2 para que nos retorne el numero no mas uwu
                    drive_file_title = drive_file_info['title'][:2].replace('.', '')
                    info_drive_list.append(
                        {
                            'nombre': int(drive_file_title)-1,
                            'id': drive_file_id
                        }
                    )
                    #print(info_drive_list)
                else:
                    print("No hay información de Google Drive en este material de trabajo.")


    return info_drive_list

def uploadMaterials(creds, file_content, file_name):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": file_name}

        # Crear un archivo temporal en tu sistema de archivos local
        temp_file_path = "temp_file.pdf"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_content)

        # pylint: disable=maybe-no-member
        media = MediaFileUpload(temp_file_path, mimetype="application/pdf")
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        #print(f'File ID: {file.get("id")}')

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