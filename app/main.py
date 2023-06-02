#!/usr/bin/env python
# coding: utf-8
from feature_extraction import loudness 
from summarize import summarize_fn
from typing import Any
import uvicorn
import whisperx
import torch
from fastapi import FastAPI,UploadFile, File,Request,Form
from fastapi.staticfiles import StaticFiles
from diarize import diarize_fn
from transcribe import transcribe_audio
from assign_speakers import assign_speakers_fn
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from pydantic import BaseModel
from sentiment import sentiment_analysis
import soundfile as sf
DATABASE_URL = "postgresql://postgres:pass%40123@localhost/transcriptions"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_a, metadata = whisperx.load_align_model(language_code='en', device=device)
print(device)


class TextFile(Base):
    __tablename__ = "text_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    def __repr__(self):
        return f"<TextFile {self.filename}>"

    def save_to_db(self):
        with SessionLocal() as session:
            session.add(self)
            session.commit()
class FileStruct(BaseModel):
    filename: str
    content: str

@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root(request: Request):
    return HTMLResponse(content=open("./index.html", "r").read(), status_code=200)

@app.post('/save')
async def save_text_file(text_file: FileStruct):
    filename = text_file.filename
    content = text_file.content
    text_file = TextFile(filename=filename, content=content)
    text_file.save_to_db()
    return {'message': 'Text file saved successfully.'}

@app.post("/diarize")
async def transcribe_and_diarize(wav_file:UploadFile=File(...),labels:str=['positive', 'negative', 'neutral']) -> 'list[dict[str, Any]]':
    loudness(wav_file.filename)
    audio_file = whisperx.load_audio(str(wav_file.filename))
    transcript = await transcribe_audio(audio_file)
    aligned_segments = whisperx.align(transcript["segments"], model_a, metadata, audio_file, device, return_char_alignments=False)
    diarization_result = diarize_fn(str(wav_file.filename))
    results_segments_w_speakers = assign_speakers_fn(diarization_result, aligned_segments)
    conversation=""
    sentiment=""
    for segment in results_segments_w_speakers["segments"]:
        line=str(segment.get("speaker", "Unknown")+":"+segment["text"])
        conversation+=line
        line_sentiment=sentiment_analysis(line)
        sentiment+=f"""{line}:  label :"{line_sentiment[0]['label']} score:{line_sentiment[0]['score']}
        """
    chunk_size=400
    conversation_chunks=[conversation[i:i+chunk_size] for i in range(0, len(conversation), chunk_size)]
    summary=""
    
    sentiment=str(sentiment)
    for chunk in conversation_chunks:
        summary+=summarize_fn(chunk)[0]["summary_text"]

    text = f"""summary_text:
{summary}

conversation:
{conversation}

sentiment:
{sentiment}"""
    return text
app.post("/transcribe")
async def transcribe():
    audio_file = whisperx.load_audio(str(wav_file.filename))
    transcript = await transcribe_audio(audio_file)
    return transcript

if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000,reload=True)








