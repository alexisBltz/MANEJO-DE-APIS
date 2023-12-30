import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly",
          "https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
  creds = otorgarPermisos()
  classroom = mostrarClassroom(creds)
  print(classroom)
  drive(creds)


def drive(creds):
    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
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