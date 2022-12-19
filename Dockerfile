FROM python:3
WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD uvicorn server:app --reload --host=0.0.0.0
