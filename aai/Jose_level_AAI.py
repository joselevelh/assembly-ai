#!/usr/bin/env python
# coding: utf-8

import replicate
import streamlit as st
import requests
import aai_helpers
import os

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# Declaring Streamlit containers
st_header = st.container()
audio_source = st.container()
sum_gen = st.container()
stable_dif = st.container()
use_case = st.container()
chapter_sum = st.container()
st_footer = st.container()

with st_header:
    st.title('Using AI to paint a Podcast')
    st.markdown("This app uses [Assembly AI's](https://www.assemblyai.com/) speech-to-text API to process podcasts "
                "(or any audio) and \nsummarizes them into usable prompts for the stable diffusion art generator")
with audio_source:
    st.header('Link Audio Source')
    st.markdown("Paste a link to the audio you want the AI to paint!")
    audio_link = st.text_input('URL to Audio Source',
                               'https://www.listennotes.com/e/p/bd7844463bac4decaf480a63b121c94d/')
with sum_gen:
    st.header("Summary Generation")
    post_response = aai_helpers.post_summary(audio_url=audio_link)
    print('processing:', post_response['id'])
    get_response = aai_helpers.get(transcript_id=post_response['id'],
                                   status=post_response['status'])
    st.write(f"Here's the summary generated from AssemblyAI:  \n"
             f"\'{get_response.get('summary')}\'")
with stable_dif:
    st.header("AI Art with Stable Diffusion Model")
    st.markdown("We can now feed this summary as a prompt for stability-ai's [stable "
                "diffusion](https://replicate.com/stability-ai/stable-diffusion) model")
    model = replicate.models.get("stability-ai/stable-diffusion")
    st.markdown(
        "I will be spicing up the prompt by including a set prefix. Feel free to add your own prefix by typing it below!")
    prefix = st.text_input('Prompt prefix', 'Photorealistic painting of ')
    st.markdown(get_response.get('summary'))
    output = model.predict(prompt=prefix + get_response.get('summary'))
    st.image(output[0])
with use_case:
    st.header("Possible Use Cases")
    st.write("Some possible use cases for this app flow:")
    st.markdown("- Thumbnail generator for your podcast or audiobook")
    st.markdown("- Visual summaries for your content")
    st.markdown("- Modified single player version of the popular game [Gartic Phone](https://garticphone.com/)")
    st.markdown("- Just messing around (although it does cost me ~.20 cents every time this runs)")
with chapter_sum:
    st.header("Using Chapter Summaries to Make an Art Series!")
    st.markdown("Now lets take this one step further and use Assembly AI to automatically create chapters and generate "
                "summaries for each section. Then we will feed *those* into stable diffusion to make a series of "
                "paintings")
    st.markdown("I will give you another chance to use your own audio file here, if not we will use the default.")
    new_audio_link = st.text_input('URL to Audio Source for series',
                                   'https://www.listennotes.com/e/p/bd7844463bac4decaf480a63b121c94d/')
    post_chapters_response = aai_helpers.post_chapters(audio_url=audio_link)
    print('processing:', post_chapters_response['id'])
    get_chapters_response = aai_helpers.get(transcript_id=post_chapters_response['id'],
                                            status=post_chapters_response['status'])
    st.markdown("For speed (and cost)'s sake I am only going to feed the first 5 chapters into the AI art generator  \n"
                "but don't worry, you will still get some cool results!")
    max_chapters = 5  # Limiting chapter count so we don't spend a really long time generating images
    chapter_count = 0
    for chapter_info in get_chapters_response.get("chapters"):
        if chapter_count < max_chapters:
            st.write(f"Summary of chapter {chapter_count+1}:  \n"
                     f"\'{chapter_info.get('summary')}\'")
            output = model.predict(prompt=prefix + chapter_info.get('summary'))
            st.image(output[0])
        else:
            print("Exceeded max chapter count")
        chapter_count += 1
    st.markdown("That's more like it!")
with st_footer:
    st.header("You've reached the end!")
    st.markdown("Thanks for trying out this dashboard! If you want to see the code for this project checkout the [github](https://github.com/joselevelh/assembly-ai)."
                "If you are interested to see other things I've made, check out my [website](https://joselevel.com/)")
