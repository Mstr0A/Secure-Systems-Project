FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY . .

RUN uv sync

EXPOSE 5050

CMD [ "uv", "run", "main.py" ]