FROM python:3.9
ENV PYTHONPATH /usr/src/app
WORKDIR /app
ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672
ENV RABBITMQ_USERNAME=guest
ENV RABBITMQ_PASSWORD=guest
ENV RABBITMQ_QUEUE=pc
ADD consumer.py /app
EXPOSE 9422
CMD ["python", "consumer.py"]

