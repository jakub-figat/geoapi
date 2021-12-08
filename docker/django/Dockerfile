FROM python:3.9.5

ARG ENV

ENV ENV="$ENV" \
PYTHONFAULTHANDLER=1 \
PYTHONUNBUFFERED=1 \
PYTHONHASHSEED=random \
# pip
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=1 \
# poetry
POETRY_VERSION=1.1.7 \
POETRY_VIRTUALENVS_CREATE=false \
POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /app

RUN apt-get update -q && apt-get install -yq netcat

COPY ./pyproject.toml ./poetry.lock ./
RUN pip install poetry==$POETRY_VERSION

RUN poetry install $(if [ "$ENV" = 'prod' ]; then echo "--no-dev"; fi) --no-ansi --no-interaction

COPY ./scripts/wait_for_db.sh /wait_for_db.sh

RUN chmod +x /wait_for_db.sh

COPY . .

ENTRYPOINT ["sh", "/wait_for_db.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]