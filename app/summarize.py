from transformers import pipeline
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")
def summarize_fn(result):
    summary=summarizer(result)
    return summary