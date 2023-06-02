from transformers import pipeline
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
sentimenter=pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def sentiment_analysis(text):
    sentiment=sentimenter(text)
    print(sentiment)
    return sentiment