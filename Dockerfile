FROM python:3.8

WORKDIR /app

COPY requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.dev.txt

COPY . .

CMD ["python", "gradio_app.py"]
