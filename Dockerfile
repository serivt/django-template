FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

ENV ENV /etc/profile

RUN mkdir /logs

COPY . /app

COPY profile.d/* /etc/profile.d/

WORKDIR /app

RUN apk update \
    # psycopg2 dependencies
    && apk add --virtual .build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev git curl \
    # CFFI dependencies
    && apk add libffi-dev py-cffi \
    && apk add libc-dev binutils \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
    && source $HOME/.poetry/env \
    && poetry install \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
