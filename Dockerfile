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
