FROM python:3.9-alpine
WORKDIR /app
ADD . /app
RUN python -m venv venv
RUN source ./venv/bin/activate
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN crontab crontab
CMD [ "crond", "-f" ]