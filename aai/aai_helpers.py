import requests
from time import sleep
import streamlit as st

# global variables
base_endpoint = 'https://api.assemblyai.com/v2'
headers = {'authorization': st.secrets["AAI_API_TOKEN"]}


# function to send audio to assemblyai
def post_summary(audio_url):
    payload = {"audio_url": audio_url,
               "summarization": True,
               "summary_type": "paragraph"}
    response = requests.post(f'{base_endpoint}/transcript',
                             json=payload,
                             headers=headers)
    return response.json()


def post_chapters(audio_url):
    payload = {"audio_url": audio_url,
               "auto_chapters": True,}
    response = requests.post(f'{base_endpoint}/transcript',
                             json=payload,
                             headers=headers)
    return response.json()


# function to poll assemblyai for transcript
def get(transcript_id, status):
    current_status = status
    while current_status != 'completed':
        response = requests.get(f'{base_endpoint}/transcript/{transcript_id}',
                                headers=headers)
        current_status = response.json()['status']
        print(f"Current Status: {current_status}...")
        sleep(3)
    return response.json()
