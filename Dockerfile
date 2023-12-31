FROM alpine:3.18

RUN apk add --no-cache python3 python3-dev py3-pip

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 1000

CMD ["/app/venv/bin/gunicorn", "--bind", "0.0.0.0:1000", "app:app"]

