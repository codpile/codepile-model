FROM alpine:3.18

RUN apk add --no-cache python3=3.9.7-r3 python3-dev=3.9.7-r3 py3-pip=20.3.4-r1

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 1000

CMD ["/app/venv/bin/gunicorn", "--bind", "0.0.0.0:1000", "app:app"]
