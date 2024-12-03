FROM documentor:0.0.4
#FROM  ollama/ollama:latest
WORKDIR /docu-mentor-service
COPY documentor.tar.gz /docu-mentor-service/
RUN tar -zxvf /docu-mentor-service/documentor.tar.gz

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tar \
    && apt-get clean
RUN pip install -r /docu-mentor-service/documentor/requirements.txt
#WORKDIR /app
COPY start.sh /docu-mentor-service/documentor/start.sh
RUN chmod +x /docu-mentor-service/documentor/start.sh
#ENTRYPOINT ["/app/start.sh"]
