# pull official base image
FROM python:3.8.0-alpine
# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN /sbin/apk add --no-cache --virtual .deps gcc musl-dev \
 && /usr/local/bin/pip install --no-cache-dir black==19.10b0 \
 && /sbin/apk del --no-cache .deps
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
