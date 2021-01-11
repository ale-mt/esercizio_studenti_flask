FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

RUN useradd appuser && chown -R appuser /usr/src/app
USER appuser

CMD [ "python", "./app.py" ]
