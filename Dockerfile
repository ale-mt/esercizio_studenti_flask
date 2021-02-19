# docker run -itd --name student_api -p 5000:5000 -e MYSQL_HOST=172.17.0.5 student_api
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

RUN useradd appuser && chown -R appuser /usr/src/app
USER appuser

CMD [ "python", "./app.py" ]
