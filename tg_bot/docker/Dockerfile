FROM python:3.11 as base

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code
ARG APP_USER=app-user
ARG APP_USER_UID=1000

WORKDIR /code

RUN groupadd --gid ${APP_USER_UID} --system ${APP_USER} && \
    useradd --uid ${APP_USER_UID} \
            --gid ${APP_USER} \
            --system \
            --no-create-home \
            --shell /bin/false \
            ${APP_USER}

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.3.2

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev \
    && echo yes | poetry cache clear . --all


# tests image
FROM base AS test

RUN poetry install --no-interaction --no-ansi --with dev

USER ${APP_USER}
