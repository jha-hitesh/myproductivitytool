FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
RUN apt update \
    && apt install curl bash libpq-dev gcc -y

WORKDIR /srv/
COPY . /srv/

RUN pip3 install -U pip && pip3 install -r /srv/requirements.txt &&  rm -rf /root/.cache/pip/*


ENTRYPOINT ["python3.8", "manage.py", "runserver", "0.0.0.0:8000"]