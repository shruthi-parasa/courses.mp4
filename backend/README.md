Create Virtual Environment:
```bash
python -m venv venv/
```

Get inside Virtual Environment:

- Windows(cmd):
```bash
venv\Scripts\activate
```

- Mac:
```bash
source venv/bin/activate
```

Go to Backend folder:
```bash
cd backend
```

Install Python packages
```bash
pip install -r requirements.txt
```

Update requirements.txt
```bash
pip freeze > requirements.txt
```

Run unit tests:

```bash
python -m unittest discover -s tests
```