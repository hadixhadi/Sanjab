FROM python:3.10.6
LABEL authors="hadi"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR src
COPY ./requirments /requirments
COPY ./src /src

EXPOSE 8000

RUN pip install -r /requirments/requrments.txt
CMD python src/manage.py migrate