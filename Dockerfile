FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=host.docker.internal:0

CMD ["python", "crypto_list.py"]