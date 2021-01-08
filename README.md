# esercizio_studenti_flask
## In __init__.py edit db configuration line:
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@ip_address/db_name'
```

## Dockerfile:

```
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run.py" ]
```

## Build:
```
$ docker build -t my-python-app . 
```

## Run:
```
$ docker run -it --rm --name my-running-app my-python-app 
```
