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

st.markdown("""
            
    #### How to use this application
            
    - Record your audio to start the conversation.
    - You can also see the conversation history on sidebar.
    - After clicking on `Delete Conversation` button, refresh the page to start a new conversation.
            """)


tempDir = 'tempDir'
if not os.path.exists(tempDir):
    os.makedirs(tempDir)

file = 'responses.txt'


# setting up the OpenAI API Key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


#  ChatBot
def chatagent():
    chatbot = ChatBot.pdf_chat(
        input_files=[Path('./data/restaurant data.pdf')], system_prompt=utils.system_prompt(),
    ) 
    return chatbot


# Voice bot
def voiceagent(audio_bytes):
    voice = VoiceBot()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        # Save the recorded audio for transcription
        with open('tempDir/output.wav', 'wb') as f:
            f.write(audio_bytes)
        audiopath = 'tempDir/output.wav'
        if audiopath:
            user_input = voice.transcribe(audiofilepath='tempDir/output.wav')
            # st.write(user_input)
                
        chatbot = chatagent()
        response = chatbot.chat(user_input)
        voice.text_to_speech(response.response)
        utils.write_to_file(user_input=user_input, chatbot_response=response.response, file_path=file)
        # st.text(response.response)
        tts_audio_file = 'tts_output.mp3'
        if os.path.isfile(tts_audio_file):
            st.audio(tts_audio_file, format='audio/mp3', start_time=0)
    
    else:
        st.warning('Record your audio to start the conversation')


def delete_conversation():
        os.remove('tts_output.mp3')
        os.remove(file)
        st.warning('Record your audio to start the conversation')


if __name__ == "__main__":
    audio_bytes = audio_recorder()
    voiceagent(audio_bytes)


    if os.path.exists(file):
        if st.button('Delete Conversation'):
            delete_conversation()
        

    if os.path.exists(file):
        chat_history = utils.read_chat_history(file_path=file)
        st.sidebar.subheader("Conversation History")
        for line in chat_history:
            st.sidebar.write(line.strip())

    utils.template_end()
            


  
    