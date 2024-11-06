FROM python:3.9

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["streamlit", "run", "--server.port", "8080", "app/app.py"]
