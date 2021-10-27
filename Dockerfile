FROM python:3.9
ENV PYTHONUNBUFFERED=1
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
WORKDIR /src
COPY /src/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY ./src .
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
RUN mkdir -p /usr/local/var/log/gunicorn
ENTRYPOINT [ "./entrypoint.sh" ]
