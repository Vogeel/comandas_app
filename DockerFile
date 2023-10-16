#
FROM python:3.11-slim

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
COPY ./scr /code

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
ENTRYPOINT ["python"]
CMD ["main.py"]