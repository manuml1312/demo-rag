# Second
import streamlit as st 
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import ServiceContext
from llama_index.llms import Replicate


REPLICATE_API_TOKEN = "r8_VIpRfodHy75ZM7GUguQM56Zz44Sa4G10p4Eku"

st.title("📝 File Q&A ") 
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md")) 
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

llama2_7b_chat = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"
llm = Replicate(
    model=llama2_7b_chat,
    temperature=0.01,
    additional_kwargs={"top_p": 1, "max_new_tokens": 300},
)

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

service_context = ServiceContext.from_defaults(
    llm=llm, embed_model=embed_model
)

documents = SimpleDirectoryReader("/content/").load_data()
index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

# client = anthropic.Client(api_key=anthropic_api_key)
index.storage_context.persist()
query_engine = index.as_query_engine(service_context=service_context)
response=query_engine.query("What is chain of thought fine tuning mixture?")

st.write("### Answer")
st.write(response)
