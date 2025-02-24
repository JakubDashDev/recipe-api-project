#using alpine because is super lightweight 
FROM python:3.9-alpine3.13
LABEL maintainer="Jakub Cieślik"

#disable buffer and shows logs immediately in the console
ENV PYTHONBUFFERED 1

#copy necessary files to tmp catalog
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

#setting app folder as current work directory
WORKDIR /app

#exposing port
EXPOSE 8000

#setting development mode to false -> overwrite it in docker-compose
ARG DEV=false

#creating virtual env 
#updating pip
#installing dependencies
#deleting tmp after installation
#creating user without password and home folder named "django-user"
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#saving base path to variable
ENV PATH="/py/bin:$PATH"

#switching to new user -> don't use root user due to security reasons
USER django-user