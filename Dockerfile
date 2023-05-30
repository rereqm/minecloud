FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

#setup cron
COPY decrease_server_days_cnt /etc/cron.d/decrease_server_days_cnt
RUN chmod 0644 /etc/cron.d/decrease_server_days_cnt
RUN crontab /etc/cron.d/decrease_server_days_cnt
RUN touch /var/log/cron.log
RUN env >> /etc/environment 


RUN useradd -rms /bin/bash app && chmod 777 /opt /run

#setup app
WORKDIR /app

COPY --chown=app:app ./app .

RUN pip install -r requirements.txt

RUN mkdir -p /app/static && mkdir -p /app/media
RUN chmod -R 755 /app && chown -R app:app /app


#USER app