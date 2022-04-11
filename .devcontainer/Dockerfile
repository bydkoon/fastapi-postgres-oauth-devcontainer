# [Choice] Python version: 3, 3.8, 3.7, 3.6
ARG VARIANT=3.8

FROM python:${VARIANT}


RUN apt-get update

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt && rm requirements.txt; fi

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]


