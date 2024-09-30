# docker build -t redis-proxy .
# docker run -d --name redis-proxy -p 8000:8000 redis-proxy
FROM python:3.10.11
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0",  "--port", "8000"]
EXPOSE 8000