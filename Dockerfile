FROM python:3

RUN useradd appuser
USER appuser
  
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser /usr/src/app

CMD [ "python", "./app.py" ]
