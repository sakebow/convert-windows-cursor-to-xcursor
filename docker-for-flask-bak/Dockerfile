FROM ubuntu:20.04
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install libconfig-inifiles-perl perlmagick imagemagick x11-apps unzip redis-server nginx -y

WORKDIR /usr/local/src/
COPY 104659-sd2xc-2.5.pl .
COPY app.py .
COPY index.html .
COPY config.yml .

RUN rm /etc/redis/redis.conf
COPY redis.conf /etc/redis/
RUN service redis restart
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN service nginx restart

RUN nohup celery -A app.celery worker --loglevel=info -B >./celery.log 2>&1 &
RUN nohup gunicorn -b 0.0.0.0:40080 app:app > app.log 2>&1 &