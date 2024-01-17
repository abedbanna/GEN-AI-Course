from django.shortcuts import render
from transformers import pipeline


def classify_text(text):
    model_id = "abedbanna/distilbert-base-uncased-finetuned-emotion"
    classifier = pipeline("text-classification", model=model_id)
    # preds = classifier(text, return_all_scores=True)
    outputs = classifier(text)
    # label = outputs.get('label')
    index = outputs[0]['label'][6:]

    return index


# Create your views here.
def index(request):
    response=""
    if request.method == 'POST':
        emotion=['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
        response=classify_text(request.POST['inputText'])
        response= emotion[int(response)]
    return render(request,context={"response":response},template_name='index.html')
