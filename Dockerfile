FROM python:3.7-slim
RUN apt-get update && apt-get install -y build-essential
RUN apt-get -y install nano curl
RUN mkdir -p /var/www/html
COPY requirements.txt /var/www/html
WORKDIR /var/www/html
RUN pip3 install -r requirements.txt
COPY . /var/www/html
EXPOSE 80
CMD ["python", "app.py"]