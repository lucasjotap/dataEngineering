ARG AWS_ACCOUNT_NUMBER
ARG ENVIRONMENT

FROM python:3.8

ARG BASE_DIR=/dbt_arc
ENV BASE_DIR=$BASE_DIR
ENV IMAGE_REPOSITORY dbt_arc-image

RUN mkdir $BASE_DIR
COPY ./dbt_arc $BASE_DIR
COPY ./requirements.txt $BASE_DIR/requirements.txt

RUN pip install -r $BASE_DIR/requirements.txt
WORKDIR $BASE_DIR