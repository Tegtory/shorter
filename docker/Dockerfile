FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip && pip install uv

COPY . .

EXPOSE 9123

CMD ["python", "main.py"]
