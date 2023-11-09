# Second
import streamlit as st 
import os
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader , Document
from llama_index.embeddings import HuggingFaceEmbedding 
from llama_index import ServiceContext
from llama_index.llms import OpenAI

openai.api_key = st.secrets.openai_key #
# openai.api_key=os.envget("openai_key")  #st.secrets.openai_key

st.title("📝 File Q&A ") 

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the Oil Well Integrity Manual!"}
    ]
    
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3, system_prompt="""You are an expert on the Oil Well Integrity manual and your job is to answer 
          all questions. Assume that all questions are related to the Well integrity of an Oil well. Keep your answers accurate and based on 
                   facts – do not hallucinate features.""")

service_context = ServiceContext.from_defaults(llm=llm) 
# reader = SimpleDirectoryReader(input_dir="./data")
reader=SimpleDirectoryReader(commit_sha="3c5afe61f3166455c1e7c593359dd315a0c4000b")
documents=reader.load_data() 
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# st.text_input("Ask me something about Oil Well Integrity",placeholder="Your Question here")

# if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
if prompt :=st.text_input("Ask me something about Oil Well Integrity",placeholder="Your Question Here"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
