from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
# case 1
chunk_size=10
chunk_overlap=4

r_splitter= RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,

)

c_splitter=CharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    # separator=''



)
# text1 = 'abcdefghijklmnopqrstuvwxyz'
# print(r_splitter.split_text(text1))
# print("*"*100)
# print(c_splitter.split_text(text1))
#
# # Recursive text Splitter
# text3 = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
# print(r_splitter.split_text(text3))
# #
# # Character Text Splitter
# print(c_splitter.split_text(text3))


#Case 2
# some_text = """When writing documents, writers will use document structure to group content. \
# This can convey to the reader, which idea's are related. For example, closely related ideas \
# are in sentances. Similar ideas are in paragraphs. Paragraphs form a document. \n\n  \
# Paragraphs are often delimited with a carriage return or two carriage returns. \
# Carriage returns are the "backslash n" you see embedded in this string. \
# Sentences have a period at the end, but also, have a space.\
# and words are separated by space."""
#
# print(len(some_text))
#
#
# c_splitter = CharacterTextSplitter(
#     chunk_size=20,
#     chunk_overlap=10,
#     separator = ' '
# )
# r_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=20,
#     chunk_overlap=10,
#     separators=["\n\n", "\n", " ", ""]
# )
# print(r_splitter.split_text(some_text))
# print("*"*100)
# print(c_splitter.split_text(some_text))


from langchain.document_loaders import PyPDFLoader
# loader=PyPDFLoader("docs/paper.pdf")
# docs=loader.load()
# #
# # print(len(docs))
# # print(docs[1])
# #
#case 3
text1 = "foo bar bazzyfoo"
from langchain.text_splitter import TokenTextSplitter
token_splitter=TokenTextSplitter(chunk_size=1,chunk_overlap=0)
# print(token_splitter.split_text(docs[0]))
print(token_splitter.split_text(text1))

loaders=[
    PyPDFLoader('docs/paper.pdf'),
    PyPDFLoader('docs/paper.pdf')


]

docs=[]
for loader in loaders:
    docs.extend(loader.load())

# Define the Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)


#
# #Create a split of the document using the text splitter
splits = text_splitter.split_documents(docs)
#
#
# from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings
# embedding = OpenAIEmbeddings()
#
# persist_directory = 'docs/chroma/'
#
# # Create the vector store
# vectordb = Chroma.from_documents(
#     documents=splits,
#     embedding=embedding,
#     persist_directory=persist_directory
# )
#
# print(vectordb._collection.count())

