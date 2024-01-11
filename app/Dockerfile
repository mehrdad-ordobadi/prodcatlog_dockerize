FROM python:3.11-alpine

# Install build dependencies
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

WORKDIR /usr/app/src

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001