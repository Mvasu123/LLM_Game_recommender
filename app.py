import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import CSVLoader

# Set the page config at the top
st.set_page_config(
    page_title="GAME Recommendation System", page_icon="🎮"
)

# Function to train and return the FAISS index
@st.cache_resource
def train_faiss():
    # Specifying the encoding while loading the CSV file
    loader = CSVLoader(file_path="games.csv", encoding="utf-8")
    documents = loader.load()

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    return db

# Load the FAISS index (train if not cached)
db = train_faiss()

# Function for similarity search
def retrieve_info(query, k=10):
    similar_response = db.similarity_search(query, k=k)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

# Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

template = """
You are a game recommendation system. 
I will share a user's message with you and you will give me the best answer that 
I should send to this user suggesting him some games based on his requirements 
and you will follow ALL of the rules below:

1/ always priortise the genre or category suggested by the user 

2/ then try to give result based on the their rating and then on the number of installs

Below is a message I received from the user:
{message}

Here is a list of best practices of how we normally respond to prospects in similar scenarios:
{best_practice}

Please write the best response that I should send to this user:
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Retrieval augmented generation
def generate_response(message):
    # Extract the number of games requested by the user
    try:
        k = int(message.split()[-1])
        message = ' '.join(message.split()[:-1])
    except:
        k = 10  # Default to 3 if no number is specified

    best_practice = retrieve_info(message, k=k)
    response = chain.run(message=message, best_practice=best_practice)
    return response

# Build an app with Streamlit
def main():
    st.header("Game Recommender Bot 🎮")
    message = st.text_area("What's on your mind?")

    if message:
        st.write("Finding Perfect Games for YOU!!!...")

        result = generate_response(message)

        st.info(result)

if __name__ == '__main__':
    main()
