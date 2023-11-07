FROM ubuntu:latest

RUN apt update
RUN apt install python3 python3-pip -y

WORKDIR /secure_gate

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 7878

CMD ["python3", "-m", "apps.server.rpc.rpc_server"]