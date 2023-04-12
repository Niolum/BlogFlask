FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt-get update
WORKDIR /blogflask
COPY requirements.txt /blogflask/
RUN pip install -r requirements.txt
COPY . /blogflask/
EXPOSE 5000