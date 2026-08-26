
FROM python:3.12-slim

WORKDIR /home/myapp


RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip "setuptools>=78.1.1" "msgpack>=1.2.1"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "sample_app.py"]