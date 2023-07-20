import streamlit as st
from streamlit_chat import message
import openai
from qa import QA
import tempfile
import os

temp_path = None
qa = None

openai.api_key = st.secrets["OPENAI_API_KEY"]


st.set_page_config(page_title="CS Automation chatbot", page_icon=":robot:")

st.header("CS Automation chatbot")

# Add content to the sidebar
st.sidebar.title("Add your CSV macro file")

# Add a file uploader field in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

# Process the uploaded file if it exists
if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    qa = QA(file_path=temp_path)

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


user_input = get_text()

if user_input:
    if qa is None:
        output = "Please load a CSV file first"
    else:
        output = qa.run_query(user_input)["answer"]

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
