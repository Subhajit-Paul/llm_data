FROM python:3.11

WORKDIR /APIEndpoints
COPY ./requirements.txt /APIEndpoints/requirements.txt
RUN python3 -m pip install --upgrade -r /APIEndpoints/requirements.txt

COPY . /APIEndpoints
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]