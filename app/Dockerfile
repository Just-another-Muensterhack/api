ARG PY_VERSION="3.10"

FROM python:${PY_VERSION}-alpine as builder

# set work directory
WORKDIR /build

RUN apk update \
 && apk add gcc g++ python3-dev musl-dev jpeg-dev zlib-dev postgresql-dev

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install --prefix=/build/venv -r requirements.txt

FROM python:${PY_VERSION}-alpine

ENV POSTGRES_PORT 5432

# create the app user and directories
ENV HOME=/home/app APP_HOME=/home/app/web
RUN mkdir -p ${HOME} \
 && mkdir -p ${APP_HOME} \
 && addgroup -S app \
 && adduser -S app -G app
WORKDIR ${APP_HOME}

# install database dependencies
RUN apk add --no-cache libpq

COPY --from=builder /build/venv/ /usr/local/

# copy project
COPY --chown=app:app . ${APP_HOME}

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
EXPOSE 8000
USER app
