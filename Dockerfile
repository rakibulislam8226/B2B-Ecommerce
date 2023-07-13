FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /src

# port where the Django app runs  
EXPOSE 8000  
COPY . .
COPY ./requirements.txt /requirements.txt 
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt


RUN adduser -D user
USER user