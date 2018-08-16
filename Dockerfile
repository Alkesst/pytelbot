FROM python:3.6

RUN mkdir -p /app/pytel_bot
WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt && \
    apt-get install -y --no-install-recommends fonts-liberation && \
    apt-get clean && \
    rm -rf /var/lib/apt && \
    rm -rf /var/cache/apt

COPY main.py insultos.txt useless_data.txt insults.txt ./
COPY pytel_bot ./pytel_bot/

CMD python main.py
