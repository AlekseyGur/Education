FROM debian:stable
RUN sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get install -y default-jdk maven
COPY . /app
WORKDIR /app
RUN bash /app/mvnw clean package
ENTRYPOINT ["java"]
CMD ["-jar", "/app/target/titanic-predict-0.0.1.jar"]
