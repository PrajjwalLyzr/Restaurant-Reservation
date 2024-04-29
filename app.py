from utils import utils
import streamlit as st
from lyzr import ChatBot, VoiceBot
import os
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()
from audio_recorder_streamlit import audio_recorder

utils.page_config()
utils.style_app()

# Streamlit app interface
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)
st.title('Restaurant-Reservation Chatbot')
st.markdown('Welcome to the lyzr Restaurant-Reservations app, this app will help you to handle restaurant reservations !!!')


if not os.path.exists('tempDir'):
    os.makedirs('tempDir')

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Initialize the system prompt
system_prompt = """
Your name is Eva.
You are the Manager at Gourmet Delight restaurant.
You represent the Gourmet Delight restaurant.
Start with any of the following greeting messages
“Hi, I am Eva, Manager at Gourmet Delight restaurant. How can I help you?”
Output Length: Keep your answers less than 30 words so that it sounds more natural chat.
Your Persona: Iris is a middle-aged woman born in the US. She is friendly, with a great sense of humor that is understated and professional, but she understands that making people comfortable includes using humor.
"""
file = 'responses.txt'

# ChatBot
def chatagent():
    chatbot = ChatBot.pdf_chat(
        input_files=[Path('data/restaurant data.pdf')], system_prompt=system_prompt,
    ) 
    return chatbot

# Voice bot
voice = VoiceBot()
audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    # Save the recorded audio for transcription
    with open('tempDir/output.wav', 'wb') as f:
        f.write(audio_bytes)
    audiopath = 'tempDir/output.wav'
    if audiopath:
        user_input = voice.transcribe(audiofilepath='tempDir/output.wav')
        st.write(user_input)
            
if st.button('Send'):
    chatbot = chatagent()
    response = chatbot.chat(user_input)
    voice.text_to_speech(response.response)
    utils.write_to_file(user_input=user_input, chatbot_response=response.response, file_path=file)
    st.text(response.response)
    tts_audio_file = 'tts_output.mp3'
    if os.path.isfile(tts_audio_file):
        st.audio(tts_audio_file, format='audio/mp3', start_time=0)

if os.path.exists(file):
    chat_history = utils.read_chat_history(file_path=file)
    st.sidebar.subheader("Conversation History")
    for line in chat_history:
        st.sidebar.write(line.strip())


if os.path.exists("tts_output.mp3"):
    st.error('Be carefull while click on this button !!!')
    if st.button('Delete Conversation'):
        os.remove('tts_output.mp3')
        os.remove(file)
        st.rerun()

utils.template_end()
            


            
    