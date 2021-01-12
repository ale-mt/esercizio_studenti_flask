FROM python:3

RUN useradd appuser && chown -R appuser /usr/src/app
USER appuser
  
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
