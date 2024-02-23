from api_communication import *
import streamlit as st
import json


st.title('Big Z Podcast SummariZer')
episode_id = st.sidebar.text_input('Please enter an episode ID:')
button = st.sidebar.button('Fetch Podcast Summary', on_click=save_transcript, args=(episode_id, True, ))

def get_clean_time(time_ms):
    seconds = int((time_ms / 1000) % 60)
    minutes = int((time_ms / (1000 * 60)) % 60)
    hours = minutes = int((time_ms / (1000 * 60 * 60)) % 60)

    if hours > 0:
        start_time = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_time = f'{minutes:02d}:{seconds:02d}'
    
    return start_time
 
if button:
    filename = episode_id + '_chapters.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        chapters = data['chapters']
        podcast_title = data['podast_title']
        episode_title = data['episode_title']
        thumbnail = data['episode_thumbnail']

    st.header(f'{podcast_title} - {episode_title}') 
    st.image(thumbnail)

    for ch in chapters:
        with st.expander(ch['gist'] + ' - ' + get_clean_time(ch['start'])):
            ch['summary']

# episode_id = 'cd379c36abd94d32a1b3fbbadf26b597'
# success_checker = save_transcript(episode_id, True)
# if success_checker:
#     print('Podcast summarization was a success')
# else:
#     print('Sorry but we encountered some issues!')