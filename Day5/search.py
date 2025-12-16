from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
#pip install langchain-core
persist_directory = 'docs/chroma/'
os.environ['OPENAI_API_KEY'] = ''

embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectordb.as_retriever()

question = "what are the datasets used in this paper"

llm = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate.from_template("""
Answer the question based on the following context:

Context: {context}

Question: {question}

Answer:
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke(question)
print(result)
