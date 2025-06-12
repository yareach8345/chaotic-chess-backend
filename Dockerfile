FROM python:3.12.3

WORKDIR /chaotic-chess

COPY ./requirements.txt /chaotic-chess/requirements.txt

COPY ./main.py /chaotic-chess/main.py

RUN pip install --no-cache-dir --upgrade -r /chaotic-chess/requirements.txt

COPY ./app /chaotic-chess/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]