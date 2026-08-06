#!/bin/bash


docker stop app-backend 2>/dev/null && docker rm app-backend 2>/dev/null
docker rmi app-backend-img 2>/dev/null
rm -rf tempdir


mkdir -p tempdir/templates
mkdir -p tempdir/static


cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.


echo "FROM python" > tempdir/Dockerfile
echo "RUN pip install flask pymysql" >> tempdir/Dockerfile
echo "COPY ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 5050" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/sample_app.py" >> tempdir/Dockerfile


cd tempdir
docker build -t app-backend-img .
docker run -d -p 5050:5050 --network red-cba --name app-backend app-backend-img
