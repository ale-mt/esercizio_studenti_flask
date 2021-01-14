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

EXPOSE 8080

CMD [ "python", "./app.py" ]

```

## Build:
```
$ docker build -t my-python-app . 
```

```
oc new-app https://github.com/ale-mt/esercizio_studenti_flask#openshift_deploy -e MYSQL_USER=root -e MYSQL_PASSWORD=password -e MYSQL_SERVICE_HOST=host -e MYSQL_DATABASE=flask_mysql -l app=studenti-python --name=studenti --image-stream=openshift/python
```

it is possible to not specify a value for ```MYSQL_SERVICE_HOST``` and let oc manage it

## Run:
```
$ docker run -it --rm --name my-running-app my-python-app 
```
```
oc expose svc/studenti
```
