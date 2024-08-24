FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN black .
RUN isort .
CMD ["python3", "jobot.py"]