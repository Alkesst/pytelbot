FROM python:3.6

RUN mkdir -p /app/pytel_bot
WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY main.py insultos.txt useless_data.txt insults.txt ./
COPY pytel_bot ./pytel_bot/

CMD python main.py
