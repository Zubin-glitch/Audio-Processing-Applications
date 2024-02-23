import requests
from api_info import API_KEY_AAI, API_KEY_LISTENNOTES
import time
import json
import pprint

# episode_id = cd379c36abd94d32a1b3fbbadf26b597

transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
listennotes_episode_endpoint = 'https://listen-api.listennotes.com/api/v2/episodes'

aai_auth_header = {"authorization": API_KEY_AAI}
listennotes_auth_header = {"X-ListenAPI-Key": API_KEY_LISTENNOTES}

def get_episode_audio_url(episode_id):
    episode_url = listennotes_episode_endpoint + '/' + episode_id
    response = requests.request('GET', episode_url, headers=listennotes_auth_header)

    response_data = response.json()
    # pprint.pprint(response_data)
    audio_url = response_data['audio']
    episode_thumbnail = response_data['thumbnail']
    podcast_title = response_data['podcast']['title']
    episode_title = response_data['title']

    return audio_url, podcast_title, episode_title, episode_thumbnail


# transcribe the audio file

def transcribe(audio_url, auto_chapters):
    transcript_request = {"audio_url": audio_url,
                          "auto_chapters": auto_chapters}
    transcript_response = requests.post(transcript_endpoint , json=transcript_request, headers=aai_auth_header)
    # print('#2\n', transcript_response.json())
    return transcript_response.json()['id']



# poll AAI repeatedly
     
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=aai_auth_header)
    return polling_response

def  get_transcription_result_url(audio_url, auto_chapters):
    transcript_id = transcribe(audio_url, auto_chapters)
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
            print("Your request is in progress...\nWaiting and retrying in 60 seconds...")
            time.sleep(60)


# save transcript to a file

def save_transcript(episode_id, auto_chapters):
    audio_url, podcast_title, episode_title, episode_thumbnail = get_episode_audio_url(episode_id)
    data, error = get_transcription_result_url(audio_url, auto_chapters=True)

    # print("Intermediate results: \n")
    # pprint.pprint(polling_response)

    if data:
        final_transcript_name = episode_id + "_transcript.txt"
        with open(final_transcript_name, 'w') as file:
            file.write(data['text'])
        chapters_file_name = episode_id + "_chapters.json"
        with open(chapters_file_name, 'w') as file:
            chapters = data['chapters']
            episode_data = {'chapters': chapters}
            episode_data['episode_title'] = episode_title
            episode_data['podcast_title'] = podcast_title
            episode_data['episode_thumbnail'] = episode_thumbnail

            json.dump(episode_data, file, indent=4)
            print("Transcript saved successfully!")
            return True
    elif error:
        print(error,"\n")
        return False
    


# --------------------------------------------------------------------------------------------------------------------------------