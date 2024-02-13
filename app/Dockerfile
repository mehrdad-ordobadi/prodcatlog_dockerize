FROM python:3.12-alpine

# Install build dependencies
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

WORKDIR /usr/app/src

COPY . .

RUN mkdir -p /var/log

RUN chmod -R 755 /var/log

RUN pip install -r requirements.txt

EXPOSE 5001