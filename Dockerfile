FROM python:3.11-slim

WORKDIR /app

COPY article_fetcher.py /app/article_fetcher.py

RUN pip install requests tqdm

ENTRYPOINT ["python", "article_fetcher.py"]