FROM python:3
LABEL version="0.0.2-alpha"
LABEL description="RPG discord bot"

ENV DATA_PATH="/data"
WORKDIR /usr/src/app
COPY . .

RUN mkdir /data
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pytest tests/

CMD ["python", "-m", "bot"]
