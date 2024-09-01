git clone ...
cd fastapi-project

1.python -m venv venv

2.source venv/bin/activate # On Windows, use `venv\Scripts\activate`

3.pip install -r requirements.txt

# Start the main server

4.python .\server.py

# Start the celery worker server

5.celery -A app.tasks.celery_app worker --loglevel=info

# start redis

6.redis-server

#check the swagger api/docs

`http://127.0.0.1:5005/docs`

## API FOR UPLOADING CSV

```
curl -X 'POST' \
  'http://127.0.0.1:5005/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test2.csv;type=text/csv'
```

## API FOR CHECKING STATUS :

````curl -X 'GET' \
 'http://127.0.0.1:5005/status/22e3321b-8c4b-467c-9009-39ec57f60cf7' \
 -H 'accept: application/json'```
````
