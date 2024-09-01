git clone ...
cd fastapi-project

1.python -m venv venv

2.source venv/bin/activate # On Windows, use `venv\Scripts\activate`

3.pip install -r requirements.txt

4.python .\server.py

http://127.0.0.1:5005/docs

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
