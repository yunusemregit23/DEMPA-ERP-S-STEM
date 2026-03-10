# DEMPA-ERP-S-STEM

Python standart kütüphanesi ile çalışan basit bir HTTP API uygulaması.

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uygulamayı çalıştırma

```bash
python -m app.main
```

Uygulama varsayılan olarak `http://0.0.0.0:8000` adresinde ayağa kalkar.

## Testler

```bash
python -m unittest discover -s tests
```
