from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
import requests
import openai

OPEN_API_KEY = ''
ASSISTANTS_API_END_POINT = 'https://api.openai.com/v1/assistants/'
VECTOR_STORES_END_POINT = 'https://api.openai.com/v1/vector_stores/'
FILES_END_POINT = 'https://api.openai.com/v1/files'
THREADS_END_POINT = 'https://api.openai.com/v1/threads/'
MESSAGES_END_POINT = 'https://api.openai.com/v1/threads/'

headers = {
    'Authorization': f'Bearer {OPEN_API_KEY}',
    'OpenAI-Beta': 'assistants=v2'
}
params = {
    'limit': 20,  # Optional: Set the limit of objects to be returned
    'order': 'desc',
}

def get_vector_stores():
    try:
        response = requests.get(VECTOR_STORES_END_POINT, headers=headers, params=params)
        print(response)
        if response.status_code == 200:
            stores = response.json()
            print(stores)
        else:
            print(f"Failed to list assistants. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to list vector stores. Error: {e}")

def create_vector_store():
    try:
        params = {
            'name': 'test-store',
            'description': 'test-store-description'
        }
        response = requests.post(VECTOR_STORES_END_POINT, headers=headers, params=params)
        print(response)
        if response.status_code == 200:
            stores = response.json()
            print(stores)
        else:
            print(f"Failed to list assistants. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to list vector stores. Error: {e}")
def get_assistants():
    try:
        response = requests.get(ASSISTANTS_API_END_POINT, headers=headers, params=params)
        print(response)
        if response.status_code == 200:
            assistants = response.json()
            print(assistants)
        else:
            print(f"Failed to list assistants. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to list assistants. Error: {e}")

def upload_file(file_path):
    try:
        file_obj = open(file_path, 'rb')
        print("FILE OBJ ", file_obj)
        file_data = {
            'file': [file_obj],
            "purpose": "assistants",
        }
        response = requests.post(FILES_END_POINT, headers=headers, files=file_data)
        if response.status_code == 200:
            uploaded_file = response.json()
            print(uploaded_file)
        else:
            print(f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
            print(f"Failed to upload file to OpenAI. Error: {e}")

def get_files():
    try:
        response = requests.get(FILES_END_POINT, headers=headers, params=params)
        print(response)
        if response.status_code == 200:
            files = response.json()
            print(files)
        else:
            print(f"Failed to list files. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to list files. Error: {e}")

def create_assistant(name, vector_store_id):
    try:
        data = {
            "model": "gpt-4-turbo",
            'name': name,
            "tools": [{"type": "file_search"}],
            "tool_resources": {"file_search": {"vector_store_ids": [vector_store_id]}},
        }
        response = requests.post(ASSISTANTS_API_END_POINT, headers=headers, json=data)
        if response.status_code == 200:
            assistant = response.json()
            print(assistant)
        else:
            print(f"Failed to create assistant. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to create assistant. Error: {e}")

# List assistants
def list_assistants(limit=20, order='desc', after=None, before=None):
    try:
        params = {
            'limit': limit,
            'order': order,
            'after': after,
            'before': before
        }
        response = requests.get(ASSISTANTS_API_END_POINT, headers=headers, params=params)
        if response.status_code == 200:
            assistants = response.json()
            print(assistants)
        else:
            print(f"Failed to list assistants. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to list assistants. Error: {e}")

def create_thread(messages=None, tool_resources=None):
    try:
        data = {
            'messages': messages,
            'tool_resources': tool_resources
        }
        response = requests.post(THREADS_END_POINT, headers=headers, json=data)
        if response.status_code == 200:
            thread = response.json()
            print(thread)
        else:
            print(f"Failed to create thread. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to create thread. Error: {e}")

def retrieve_thread(thread_id):
    try:
        endpoint = THREADS_END_POINT + thread_id
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            thread = response.json()
            print(thread)
        else:
            print(f"Failed to retrieve thread. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to retrieve thread. Error: {e}")

def create_message(thread_id, role, content):
    try:
        endpoint = MESSAGES_END_POINT + f'{thread_id}/messages'
        data = {
            'role': role,
            'content': content
        }
        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code == 200:
            message = response.json()
            print(message)
        else:
            print(f"Failed to create message. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to create message. Error: {e}")

def list_messages(thread_id, limit=20):
    try:
        endpoint = MESSAGES_END_POINT + f'{thread_id}/messages'
        params = {
            'limit': limit
        }
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            messages = response.json()
            print(messages)
        else:
            print(f"Failed to list messages. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to list messages. Error: {e}")

def create_run(thread_id, assistant_id):
    try:
        endpoint = THREADS_END_POINT + f'{thread_id}/runs'
        data = {
            'assistant_id': assistant_id
        }
        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code == 200:
            run = response.json()
            print(run)
        else:
            print(f"Failed to create run. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to create run. Error: {e}")


from typing_extensions import override
from openai import AssistantEventHandler
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
    # Then, we use the `stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
    thread = create_thread()
    assistant = list_assistants()[0]
    client = openai.Client(api_key=OPEN_API_KEY)
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="",
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
def get_drive_service():
    try:
        SCOPES = ['https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_DRIVE_CREDENTIALS_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print("This is the err ", e)
