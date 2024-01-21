from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import pinecone
os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'
import pinecone
from langchain.vectorstores import Pinecone

pinecone.init(
    api_key="KEY,
    environment="ENV"

)

llm = OpenAI(temperature=.7)
template = """You are a web developer. given a program name to learn kids programming, it is your job to write a html code of that program name.

name: {name}
code: This is html code for a program name:"""
prompt_template = PromptTemplate(input_variables=["name"], template=template)
html_chain = LLMChain(llm=llm, prompt=prompt_template)

# This is an LLMChain to write a review of a play given a synopsis.
llm = OpenAI(temperature=.7)
template = """You are python developer. Given {code}, it is your job to convert this code into python and explain it."""
prompt_template = PromptTemplate(input_variables=["code"], template=template)
python_chain = LLMChain(llm=llm, prompt=prompt_template)

# This is the overall chain where we run these two chains in sequence.
overall_chain = SimpleSequentialChain(chains=[html_chain, python_chain], verbose=True)

python_code = overall_chain.run("add two numbers")

text_splitter = RecursiveCharacterTextSplitter(
chunk_size=100,
chunk_overlap=0
)

text=text_splitter.create_documents([python_code])

print(text[0].page_content)

embedding=OpenAIEmbeddings()
query_result=embedding.embed_query(text[0].page_content)
print(query_result)

search=Pinecone.from_documents(text, embedding, index_name="test")
query="what is the  code for?"
query_result=search.similarity_search(query)
print(query_result)


