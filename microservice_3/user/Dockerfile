FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=user.py
CMD ["flask", "run", "--host=0.0.0.0","--port=5002"]
