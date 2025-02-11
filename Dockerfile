FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root 

COPY . .

CMD ["poetry", "run", "app"]