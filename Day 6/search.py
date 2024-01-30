# Load vector database that was persisted earlier and check collection count in it
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

import pinecone
from langchain.vectorstores import Pinecone

pinecone.init(
    api_key="API-Key",
    environment="gcp-starter"

)
persist_directory = 'docs/chroma/'
os.environ["OPENAI_API_KEY"] = 'API-Key'
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
# index = pinecone.Index("test")
# vectorstore = Pinecone.from_existing_index("test", embedding)
# # print(vectorstore)
# retriever = vectorstore.as_retriever()
retriever = vectordb.as_retriever()

# question = "متى يتم الاستبعاد من المنافسة"
# question = "  علي  ماذا تحتوي الكراسة"
# question = " ما  هي المنافسة "
# question="ما هي السلوكيات  و الاخلاق في هذه الكراسة"

question="what are the main contributions in this paper?"


# Similarity search with k = 5
print("*"*20,"Similarity search with k = 5","*"*20)
docs = vectordb.similarity_search(question,k=5)
print(len(docs))


# Check for first two results
print(docs[0].page_content[:100])
print(docs[1].page_content[:100])

from langchain.chains.question_answering import load_qa_chain
llm = ChatOpenAI(temperature=0.9, model_name="gpt-4")
chain=load_qa_chain(llm=llm,chain_type="stuff")
answer=chain.run(input_documents=docs,question=question)
print(answer)


print("*"*20,"Marginal relevance search","*"*20)
docs_mmr = vectordb.max_marginal_relevance_search(question,k=5)
# print(docs_mmr[0].page_content[:100])
# print(docs_mmr[1].page_content[:100])

answer=chain.run(input_documents=docs_mmr,question=question)
print(answer)


# llm = ChatOpenAI(temperature=0.9, model_name="gpt-4")
# qa_chain = RetrievalQA.from_chain_type(
#     llm,
#     retriever=retriever,
#     return_source_documents=True
# )
#
# result = qa_chain({"query": question})
# print(result["result"])
