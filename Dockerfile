FROM python:3.10.7-alpine

RUN apk add --no-cache python3-dev\
    && pip3 install --upgrade pip 

WORKDIR /run 

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . /run/

ENTRYPOINT ["python"]
CMD ["run.py"]