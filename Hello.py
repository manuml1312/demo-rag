# Second
import streamlit as st 
import os
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader , Document
from llama_index.embeddings import HuggingFaceEmbedding 
from llama_index import ServiceContext
from llama_index.llms import OpenAI

openai.api_key = st.secrets.openai_key #

st.title("📝 Material Processing Guide Chatbot ") 

# with st.sidebar:
#     st.text("Note: The material processing document \n only has details w.r.t Bayflex")

if "reader" not in st.session_state:
    st.session_state.reader = SimpleDirectoryReader(input_dir="./data")

st.write("Choose what you want to know about")
if st.button("Materials"):
    st.session_state.reader = SimpleDirectoryReader(input_dir="./data/Materials/")
if st.button("Products"):
    st.session_state.reader = SimpleDirectoryReader(input_dir="./data/Products/")
if st.button("Industries"):
    st.session_state.reader = SimpleDirectoryReader(input_dir="./data/Industries/")
if st.button("Inspiration"):
    st.session_state.reader = SimpleDirectoryReader(input_dir="./data/Inspiration/")


if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Mention your queries!"}
    ]
    
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3, system_prompt="""You are an expert on the Covestro company details which
      are mentioned in the supplied document.Answer the questions asked about the company and its products as per the supplied
      facts.Dont summarise the answers,keep them in detail and technical. Keep your answers accurate and based on 
                   facts – do not hallucinate features.""")

service_context = ServiceContext.from_defaults(llm=llm) 
documents=st.session_state.reader.load_data() 
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)


# if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
if prompt :=st.text_input("How can i help you with you today?",placeholder="Your Question Here",disabled= not documents):
    st.session_state.messages.append({"role": "user", "content": prompt})

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
