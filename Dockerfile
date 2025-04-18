# build stage
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# production stage

FROM python:3.9

WORKDIR /app

COPY . .

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update && apt-get install -y python3-tk && rm -rf /var/lib/apt/lists/*

# set env for tkinter
# This is needed to run tkinter in a docker container
ENV DISPLAY=host.docker.internal:0

# run app
CMD ["python", "crypto_list.py"]