import os
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import AmazonTextractPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser


# PDF Loader example
def configure_api():
    os.environ["OPENAI_API_KEY"] = 'API-Key'


def load_pdf(filename):
    loader = PyPDFLoader(filename)
    pages = loader.load()
    return pages

def load_ppt(filename):
    loader = UnstructuredPowerPointLoader(filename)
    pages = loader.load()
    return pages


def load_excel(filename):
    loader = UnstructuredExcelLoader(filename, mode="elements")
    pages = loader.load()
    return pages

# ! pip install yt_dlp
# ! pip install pydub
def load_youTube(url):
    save_dir = "docs/youtube/"
    loader = GenericLoader(
        YoutubeAudioLoader([url], save_dir),
        OpenAIWhisperParser()
    )
    docs = loader.load()
    return docs


def load_website(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    configure_api()
    print("Connect to Open AI")
    # pages=load_pdf("docs/spec.pdf")
    # print(len(pages))
    # print(pages[21].page_content[0:500])
    # print(pages[21].metadata)


# pip install python-pptx

    # pages=load_ppt("docs/pp.pptx")
    # print(len(pages))
    # print(pages[0].page_content[0:500])
    # print(pages[0].metadata)

    pages=load_excel("docs/pricing.xlsx")
    print(len(pages))
    print(pages[0].page_content[0:500])
    print(pages[0].metadata)


    #
    # # docs = load_youTube("https://www.youtube.com/watch?v=jGwO_UgTS7I")
    # docs = load_website(
    #     "https://sites.google.com/view/karimalbanna")
    # #
    # print(docs[0].page_content[0:500])


