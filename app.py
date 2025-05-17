import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
# for streamlit deploy secret hiding api
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel('models/gemini-2.0-flash')

st.set_page_config(page_title='Q & A Chatbot')
st.header('AI Chatbot')

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'gemini_history' not in st.session_state:
    st.session_state['gemini_history'] = []

chat = model.start_chat(history=st.session_state['gemini_history'])

def get_response(question):
    response = chat.send_message(question,stream=True)
    return response

input1 = st.text_input('How can i Help you')
button = st.button('Ask question')

if input1 and button:
    response = get_response(input1)
    st.session_state['chat_history'].append(('user',input1))
    st.session_state['gemini_history'].append({'role':'user','parts':[input1]})
    response_text = ""
    for chunk in response:
        response_text = response_text+chunk.text

    st.subheader('The Response is ')
    st.write(response_text)
    st.session_state['chat_history'].append(('Bot',response_text))
    st.session_state['gemini_history'].append({'role':'model','parts':[response_text]})

st.subheader('Chat History')
for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")





