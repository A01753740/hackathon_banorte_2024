FROM python:3.12

WORKDIR /hackathon

ADD . .

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "./app.py" ]