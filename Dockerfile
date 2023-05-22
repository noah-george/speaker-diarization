FROM python:3.10
WORKDIR /code
RUN apt-get update -qq && apt-get install ffmpeg -y
RUN pip install git+https://github.com/openai/whisper.git 
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install  git+https://github.com/m-bain/whisperx.git@v3 --upgrade
RUN pip uninstall -y SoundFile
RUN pip install SoundFile
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN apt-get update
RUN sudo apt-get -y install postgresql
COPY ./app /code/app
ENV PYTHONPATH "${PYTHONPATH}:/code/app"
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
