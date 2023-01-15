# заупскать сборку через: docker build -t predict_service .
FROM python:3.9-alpine
COPY /files/. /app
WORKDIR /app
RUN apk --no-cache add gfortran musl-dev linux-headers g++
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
