FROM python:3.10-slim-bookworm

WORKDIR /home/myapp

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Aquí va la línea RUN corregida:
RUN pip install --no-cache-dir --upgrade pip "wheel>=0.46.2" "setuptools>=84.0.0" "msgpack>=1.2.1"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "sample_app.py"]