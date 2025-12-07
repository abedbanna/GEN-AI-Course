from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from django.shortcuts import render
from django.conf import settings


# Set your OpenAI API Key
# Best practice: Use environment variable or Django settings
os.environ["OPENAI_API_KEY"] = getattr(settings, 'OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')


# Pydantic model for structured output parsing
class CustomerReview(BaseModel):
    """Customer review information extraction"""
    gift: bool = Field(description="Was the item purchased as a gift?")
    delivery_days: int = Field(description="Number of days for delivery, -1 if unknown")
    price_value: list = Field(description="Sentences about value or price")


def translate_task(chat_language, chat_text):
    """
    Translate text to specified language using OpenAI
    
    Args:
        chat_language: Target language for translation
        chat_text: Text to translate
    
    Returns:
        Translated text
    """
    # Define a template string
    template_string = """Translate the text that is delimited by triple backticks \
into a language that is {language}. 

text: ```{text}```

Provide only the translation without any additional formatting or backticks.
"""
    
    prompt_template = ChatPromptTemplate.from_template(template_string)
    
    # Create the chat model
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.0
    )
    
    # Create chain using LCEL (LangChain Expression Language)
    chain = prompt_template | chat
    
    # Invoke the chain
    response = chain.invoke({
        "language": chat_language,
        "text": chat_text
    })
    
    return response.content


def customer_feedback(customer_language, customer_email):
    """
    Generate customer service response email
    
    Args:
        customer_language: Language for the response
        customer_email: Customer's email content
    
    Returns:
        Generated response email
    """
    template_string = """You are a professional customer service representative. 
Write a response email to the customer's email that is delimited by triple backticks.

The response should be in {language}.

Customer email: ```{email}```

Provide a professional, helpful, and courteous response.
"""
    
    prompt_template = ChatPromptTemplate.from_template(template_string)
    
    # For customer service responses, use low temperature for consistency
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3
    )
    
    # Create and invoke chain
    chain = prompt_template | chat
    
    response = chain.invoke({
        "language": customer_language,
        "email": customer_email
    })
    
    return response.content


def customer_review_analysis(review_text):
    """
    Extract structured information from customer review
    
    Args:
        review_text: Customer review text
    
    Returns:
        JSON string with extracted information
    """
    review_template = """For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: ```{text}```
"""
    
    prompt_template = ChatPromptTemplate.from_template(review_template)
    
    # Set up JSON parser
    parser = JsonOutputParser(pydantic_object=CustomerReview)
    
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )
    
    # Create chain with parser
    chain = prompt_template | chat | parser
    
    try:
        response = chain.invoke({"text": review_text})
        return response
    except Exception as e:
        # Fallback to text response if JSON parsing fails
        chain_simple = prompt_template | chat
        response = chain_simple.invoke({"text": review_text})
        return response.content


# Django Views

def translate_text_view(request):
    """
    Handle translation requests
    """
    chat_language = "Arabic"
    chat_text = "My name is Abdukarim assistant professor at university of petra"
    
    if request.method == 'GET':
        chat_text = request.GET.get('message', chat_text)
        chat_language = request.GET.get('lang', chat_language)
    elif request.method == 'POST':
        chat_text = request.POST.get('message', chat_text)
        chat_language = request.POST.get('lang', chat_language)

    try:
        # Call translation function
        processed_text = translate_task(chat_language, chat_text)
        
        context = {
            'response': processed_text.replace("```", ''),
            'message': chat_text,
            'language': chat_language,
            'error': None
        }
    except Exception as e:
        context = {
            'response': '',
            'message': chat_text,
            'language': chat_language,
            'error': f'Error occurred: {str(e)}'
        }

    return render(request, context=context, template_name='translate.html')


def email_response_view(request):
    """
    Handle customer email response generation
    """
    customer_language = "Arabic"
    chat_text = "اسمي عبدالكريم البنا  اود ان  اسأل عن خدمات  شركة جوجل للمطورين"
    
    if request.method == 'POST':
        chat_text = request.POST.get('txtemail', chat_text)
        customer_language = request.POST.get('language', customer_language)

    try:
        # Generate customer response
        processed_text = customer_feedback(customer_language, chat_text)
        
        context = {
            'response': processed_text.replace("```", ''),
            'message': chat_text,
            'language': customer_language,
            'error': None
        }
    except Exception as e:
        context = {
            'response': '',
            'message': chat_text,
            'language': customer_language,
            'error': f'Error occurred: {str(e)}'
        }

    return render(request, context=context, template_name='customer_response.html')


def customer_review_view(request):
    """
    Handle customer review analysis
    """
    default_review = """This leaf blower is pretty amazing. It has four settings: \
candle blower, gentle breeze, windy city, and tornado. It arrived in two days, \
just before my wife's anniversary present. I think my wife liked it so much that \
she was speechless. So far, I've been the only one using it, and I've been using \
it every other morning to clear the leaves on our lawn. It's slightly more expensive \
than the other leaf blowers out there, but I think it's worth it for the extra features."""
    
    review = default_review
    
    if request.method == 'POST':
        review = request.POST.get('txtemail', default_review)

    try:
        # Analyze customer review
        processed_text = customer_review_analysis(review)
        
        # If response is dict (parsed JSON), convert to formatted string
        if isinstance(processed_text, dict):
            import json
            response_text = json.dumps(processed_text, indent=2, ensure_ascii=False)
        else:
            response_text = processed_text
        
        context = {
            'response': response_text,
            'message': review,
            'error': None
        }
    except Exception as e:
        context = {
            'response': '',
            'message': review,
            'error': f'Error occurred: {str(e)}'
        }

    return render(request, context=context, template_name='customer_review.html')


def index(request):
    """
    Home page view
    """
    return render(request, 'index.html')
