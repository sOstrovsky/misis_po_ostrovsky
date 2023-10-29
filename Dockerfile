FROM python:3.11

COPY ./ ./

CMD ["python3", "main.py"]