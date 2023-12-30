import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly",
          "https://www.googleapis.com/auth/drive.metadata.readonly",
          "https://www.googleapis.com/auth/classroom.courseworkmaterials"]


def main():
  creds = otorgarPermisos()
  idClassrooms = mostrarClassroom(creds)
  print(idClassrooms)
  mi_clase , clase_modelo = idClassrooms
  sacarlinksSemana(creds, idClassrooms[clase_modelo])
  #drive(creds)

def obtener_id_tema_por_nombre(creds, course_id_modelo, nombre_tema):
    service = build('classroom', 'v1', credentials=creds)

    # Obtener la lista de temas del curso
    lista_temas = service.courses().topics().list(courseId=course_id_modelo).execute()

    for tema in lista_temas.get('topic', []):
        if tema['name'] == nombre_tema:
            return tema['topicId']

    # Devolver None si no se encuentra el tema
    return None

def sacarlinksSemana(creds , course_id_modelo, topic):
    service = build('classroom', 'v1', credentials=creds)

    listaMateriales = service.courses().courseWorkMaterials().list(courseId=course_id_modelo).execute()
    print(listaMateriales)
    for material in listaMateriales['courseWorkMaterial']:
            for material_info in material['materials']:
                if 'driveFile' in material_info:
                    drive_file_info = material_info['driveFile']['driveFile']

                    drive_file_id = drive_file_info['id']
                    drive_file_title = drive_file_info['title']
                    print(f"NOMBRE: {drive_file_title}")
                    print(f"ID DRIVE: {drive_file_id}")

                else:
                    print("No hay información de Google Drive en este material de trabajo.")

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