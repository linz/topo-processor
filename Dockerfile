FROM osgeo/gdal:ubuntu-small-latest

#Install Poetry
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip install poetry
RUN poetry config virtualenvs.create false

ENV IS_DOCKER=true

#Add Poetry config and scripts
COPY . /app/topo-processor

WORKDIR /app/topo-processor

RUN poetry install --no-dev
