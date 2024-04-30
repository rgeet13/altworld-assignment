from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import FileUploadSerializer
from .utils import get_drive_service
from googleapiclient.http import MediaFileUpload
import os, requests
import openai


@api_view(['POST'])
def upload_file_to_drive(request):
    serializer = FileUploadSerializer(data=request.data)
    if serializer.is_valid():
        try:
            file = serializer.validated_data['file']
            file_path = os.path.join(settings.MEDIA_ROOT, str(file))
            print("This is the file ", file, file_path)
            
            # Check if the file exists
            if not os.path.isfile(file_path):
                raise FileNotFoundError("File not found at path: {}".format(file_path))
            
            # response = requests.get(VECTOR_STORES_END_POINT, headers=headers, params=params)
            # print(response, "OPEN AI ")
            # if response.status_code == 200:
            #     assistants = response.json()
            #     print(assistants)
            # else:
            #     print(f"Failed to list assistants. Status code: {response.status_code}, Response: {response.text}")
            
            # upload_file_to_open_ai(file_path)
            # try:
            #     file_obj = open(file_path, 'rb')
            #     print("FILE OBJ ", file_obj)
            #     file_data = {
            #         'file': (file_path, file_obj, 'application/octet-stream'),
            #         "purpose": "assistants", 
            #     }
            #     response = requests.post(FILES_END_POINT, headers=headers, files=file_data)
            #     if response.status_code == 200:
            #         uploaded_file = response.json()
            #         print(uploaded_file)
            #     else:
            #         print(f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
            # except Exception as e:
            #     print(f"Failed to upload file to OpenAI. Error: {e}")
            # # Open the file in read mode
            # with open(file_path, "r") as file:
            #     file_contents = file.read()
            #     print(file_contents)
            service = get_drive_service()
            file_metadata = {
                'name': file.name,
                'parents': ['1zVhiU_cXpemKkhFIdJUtZiqObn2LZ-3n']
            }
            # media = MediaFileUpload(file_path, mimetype=file.content_type, resumable=True)
            # res = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            # print(res)
            return JsonResponse({'message': 'File uploaded to Google Drive successfully'})
        except Exception as e:
            print("Error while uploading the file ", e)
            return JsonResponse({'error': 'Error uploading file: {}'.format(str(e))}, status=500)
    return JsonResponse(serializer.errors, status=400)


# def upload_file_to_open_ai(file_path):
#     try:
#         file_obj = open(file_path, 'rb')
#         file_data = {
#             'file': file_obj,
#             'purpose': 'assistants', 
#         }
#         response = requests.post(FILES_END_POINT, headers=headers, files=file_data)
#         if response.status_code == 200:
#             uploaded_file = response.json()
#             print(uploaded_file)
#         else:
#             print(f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
#     except Exception as e:
#         print(f"Failed to upload file to OpenAI. Error: {e}")

