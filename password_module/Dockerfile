FROM python:3.8
COPY password_module/ /
COPY requirements.txt messageBroker.py fileSystemHelper.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]