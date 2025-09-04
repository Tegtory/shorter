FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip && pip install uv

COPY . .

RUN uv sync --no-dev

EXPOSE 9123

CMD ["python", "-m", "shorter"]
