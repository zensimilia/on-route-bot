FROM python:3.9-slim
WORKDIR /bot
COPY requirements.txt /bot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /bot/
ENTRYPOINT [ "python", "bot.py" ]
