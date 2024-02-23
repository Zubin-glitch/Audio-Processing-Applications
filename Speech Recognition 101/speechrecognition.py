import requests
from api_info import API_KEY
import time

# upload the file to AAI servers through the API

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

auth_header = {"authorization": API_KEY}

def upload(filename):

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=auth_header, data=read_file(filename))

    print('#1\n',upload_response.json())

    return upload_response.json()['upload_url']


# transcribe the audio file

def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(transcript_endpoint , json=transcript_request, headers=auth_header)
    print('#2\n', transcript_response.json())
    return transcript_response.json()['id']



# poll AAI repeatedly
     
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=auth_header)
    return polling_response

def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    print(f"Transcript ID retrieved: {transcript_id}")
    while True:
        print("Polling...")
        polling_response = poll(transcript_id)
        request_status = polling_response.json()['status']
        if request_status == 'completed':
            return polling_response.json(), None            
        elif request_status == 'error':
            return polling_response.json(), 'Error retrieving transcription for audio file!' 
        else:
            print("Yet processing your request...Retrying in 5 seconds...")
            time.sleep(5)


# save transcript to a file

def save_transcript(audio_url, filename):
    polling_response, error = get_transcription_result_url(audio_url)
    resulting_text = polling_response['text']
    if error == None:
        output_file_name = filename.split('.')[0] + '.txt'
        with open(output_file_name, 'w') as out_file:
            out_file.write(resulting_text)
        
        print(f"Transcript is ready and can be viewed in {output_file_name}!")
    
    else:
        print(f"Response from polling: {polling_response} \nError?: {error}")



# --------------------------------------------------------------------------------------------------------------------------------