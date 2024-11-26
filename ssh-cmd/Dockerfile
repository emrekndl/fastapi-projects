FROM python:3.11-slim

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY ssh_cmd ./ssh_cmd

ENV PATH="/app/.venv/bin:$PATH"

RUN poetry add uvicorn

ENTRYPOINT ["python", "ssh_cmd/main.py"]

# CMD ["uvicorn", "ssh_cmd.main:app", "--host", "0.0.0.0", "--port", "8001"]
# podman run -dit --net my_custom_network --ip 172.18.0.1 -p 8001:8001 --name ssh_cmd ssh_cmd:latest
