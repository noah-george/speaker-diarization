from transformers import pipeline
summarizer = pipeline("summarization", model="amagzari/bart-large-xsum-finetuned-samsum-v2")
def summarize_fn(result):
    summary=summarizer(result)
    return summary