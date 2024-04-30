import streamlit as st


def write_to_file(user_input, chatbot_response, file_path):
    with open(file_path, 'a') as file:
        file.write("User: {}\n".format(user_input))
        file.write("Chatbot: {}\n".format(chatbot_response))
        file.write("\n")

def read_chat_history(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def system_prompt():
    sys_prompt = """
        Your name is Eva.
        You are the Manager at Gourmet Delight restaurant.
        You represent the Gourmet Delight restaurant.
        Output Length: Keep your answers less than 30 words so that it sounds more natural chat.
        Your Persona: Iris is a middle-aged woman born in the US. She is friendly, with a great sense of humor that is understated and professional, but she understands that making people comfortable includes using humor.
    """

    return str(sys_prompt)

def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 450px;
           max-width: 450px;
       }
    </style>
    """, unsafe_allow_html=True)

def page_config(layout = "centered"):
    st.set_page_config(
        page_title="Lyzr - Restaurant Reservations",
        layout=layout,  # or "wide" 
        initial_sidebar_state="auto",
        page_icon="./logo/lyzr-logo-cut.png"
    )

def template_end():
    with st.expander("ℹ️ - About this App"):
        st.markdown("This app uses Lyzr's ChatBot and VoiceBot to generate responses of user query related to the restaurant reservations.")
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)