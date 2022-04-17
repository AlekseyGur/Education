FROM debian:stable
MAINTAINER Aleksey Gur 'alexgur.work@gmail.com'
RUN sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python-dev build-essential
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["base.py"]
