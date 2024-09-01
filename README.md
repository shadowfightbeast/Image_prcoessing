git clone ...
cd fastapi-project

python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt
python .\server.py

http://127.0.0.1:5005/docs
