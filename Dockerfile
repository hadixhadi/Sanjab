FROM public.ecr.aws/docker/library/python:slim-bullseye
LABEL authors="hadi"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR src
COPY ./requirments /requirments
COPY ./src /src

EXPOSE 8000

RUN pip install -r /requirments/requrments.txt
CMD ["gunicorn","config.wsgi",":8000"]