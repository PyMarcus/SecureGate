FROM python:latest

WORKDIR /secure_gate
COPY . .

RUN pip install -r requirements.txt

EXPOSE 7878
CMD ["python", "-m", "src.apps.server.server"]
