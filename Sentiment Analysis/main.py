import json
from yt_extraction import create_audio_file
from api import save_transcript

def save_video_sentiments(video_url):
    audio_filename, audio_title = create_audio_file(video_url)
    title = audio_title.strip().replace(" ", "_")
    save_transcript(audio_filename, title, sentiment_analysis=True) 

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=oetTlR3k85I&ab_channel=TheCanadianLad"
    save_video_sentiments(video_url)
    with open("Jawan_-_Hollywood_Must_Learn!_sentiments.json", 'r') as file_json:
       data = json.load(file_json)
    
    num_of_positives = 0
    num_of_negatives = 0
    num_of_neutrals = 0
    for info in data:
        if info['sentiment'] == "POSITIVE":
            num_of_positives += 1
        elif info['sentiment'] == "NEGATIVE":
            num_of_negatives += 1
        else:
            num_of_neutrals += 1
    
    positivity_rating = (num_of_positives / len(data)) * 100
    print(f"The video you tested is {positivity_rating:.2f} Percent(%) positive!")

    print("Hope you are happy with the results!")