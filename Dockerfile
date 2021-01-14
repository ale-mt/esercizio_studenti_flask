FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd appuser
RUN chown -R appuser:appuser /usr/src/app
RUN chmod -R 777 /usr/src/app/esercizio_studenti_flask/log

USER appuser

EXPOSE 8080

CMD [ "python", "./app.py" ]
