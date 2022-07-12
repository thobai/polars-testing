FROM python:3.10.4-slim-bullseye

COPY polars_test.py /
COPY requirements.txt /

RUN pip3 install -r /requirements.txt

CMD /polars_test.py