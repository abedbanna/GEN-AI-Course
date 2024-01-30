from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
import os
os.environ["OPENAI_API_KEY"] = 'API-Key'
import pinecone
from langchain.vectorstores import Pinecone

pinecone.init(
    api_key="API-Key",
    environment="gcp-starter"

)


loaders=[
    # PyPDFLoader('docs/security.pdf'),
    PyPDFLoader('docs/paper.pdf'),
]

docs=[]
for loader in loaders:
    docs.extend(loader.load())

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=496,
    chunk_overlap=0,
    separators=["\n\n", "\n", " ", ""]
)

#
# #Create a split of the document using the text splitter
splits = r_splitter.split_documents(docs)
#
#


from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")

persist_directory = 'docs/chroma/'
#
# Create the vector store
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

print(vectordb._collection.count())

# print("*"*10,"Begin of Relevance info","*"*10)
# search=Pinecone.from_documents(splits, embedding, index_name="test")