# esercizio_studenti_flask

## Dockerfile:

```
FROM python:3

RUN echo $(whoami)

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd appuser
RUN chown -R appuser:appuser /usr/src/app
RUN chmod -R 777 /usr/src/app/esercizio_studenti_flask/log

USER appuser

RUN echo $(whoami)

RUN ls -ltr /usr/src/app

RUN ls -ltr /usr/src/app/esercizio_studenti_flask

RUN ls -ltr /usr/src/app/esercizio_studenti_flask/log/api.log

EXPOSE 5000

CMD [ "python", "./app.py" ]

```

## Build:
```
$ docker build -t my-python-app . 
```

```
oc new-app https://github.com/ale-mt/esercizio_studenti_flask#openshift_deploy -e MYSQL_HOST=mysql -e MYSQL_DATABASE=flask_mysql
 -e MYSQL_USER=root -e MYSQL_PASSWORD=**** -l app=studenti
```

## Run:
```
$ docker run -it --rm --name my-running-app my-python-app 
```
```
oc expose svc/eserciziostudentiflask
```
