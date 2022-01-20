FROM python:3.8.1
WORKDIR /Multi-ModalSummarization
COPY ./requirements.txt /Multi-ModalSummarization/requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install setuptools_rust
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt 
COPY ./ /Multi-ModalSummarization/
RUN pip install /Multi-ModalSummarization/python-client