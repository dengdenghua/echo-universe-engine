FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY echo_engine ./echo_engine
COPY agents ./agents
COPY bible ./bible
COPY characters ./characters
COPY factions ./factions
COPY locations ./locations
COPY timeline ./timeline
COPY technologies ./technologies
COPY relationships ./relationships
COPY stories ./stories
COPY prompts ./prompts
COPY workflows ./workflows
COPY asset_factory ./asset_factory

RUN pip install --no-cache-dir -e .

EXPOSE 8010

CMD ["uvicorn", "echo_engine.api:app", "--host", "0.0.0.0", "--port", "8010"]
