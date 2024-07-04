FROM python:3.11-slim

WORKDIR /app

COPY app.py /app

RUN pip install gradio==4.37.2

EXPOSE 7860

CMD ["gradio", "app.py"]