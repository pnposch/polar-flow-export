FROM python:3.9-alpine
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update 
RUN apk add chromium chromium-chromedriver git libffi-dev python3-dev gcc build-base
ENV TZ=Europe/Berlin

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
WORKDIR /polar-flow-export
ADD polar-export.py polar-export.py

CMD sleep infinity

