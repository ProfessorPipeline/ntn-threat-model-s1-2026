FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY . .
RUN useradd --uid 10001 --create-home student && chown -R student:student /app
USER student
EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"
CMD ["python", "run.py", "--host", "0.0.0.0"]
