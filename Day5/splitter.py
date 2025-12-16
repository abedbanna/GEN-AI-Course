from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
#pip install langchain-text-splitters langchain-community langchain-openai
# Your code with updated imports
chunk_size = 10
chunk_overlap = 4

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)

c_splitter = CharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)

# Rest of your code remains the same
text1 = "foo bar bazzyfoo"
token_splitter = TokenTextSplitter(chunk_size=1, chunk_overlap=0)
print(token_splitter.split_text(text1))

loaders = [
    PyPDFLoader('docs/paper.pdf'),
    PyPDFLoader('docs/paper.pdf')
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150
)

splits = text_splitter.split_documents(docs)

embedding = OpenAIEmbeddings()
persist_directory = 'docs/chroma/'

vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

print(vectordb._collection.count())
