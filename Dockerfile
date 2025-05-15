FROM python:3

RUN apt-get -yyy update && apt-get -yyy install software-properties-common && \
    wget -O- https://apt.corretto.aws/corretto.key | apt-key add - && \
    add-apt-repository 'deb https://apt.corretto.aws stable main'

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    (dpkg -i google-chrome-stable_current_amd64.deb || apt install -y --fix-broken) && \
    rm google-chrome-stable_current_amd64.deb 

# mit apt-get hat amazon coretto fehler geworfen, mit manuellem Download und dann installieren mit dpkg hat funktioniert
# RUN apt-get -yyy update && apt-get -yyy install java-1.8.0-amazon-corretto-jdk ghostscript
RUN wget https://corretto.aws/downloads/latest/amazon-corretto-8-x64-linux-jdk.deb
RUN apt-get -yyy update && apt-get -yyy install java-common
RUN dpkg --install amazon-corretto-8-x64-linux-jdk.deb

RUN pip install anvil-app-server
RUN anvil-app-server || true

VOLUME /apps
WORKDIR /apps

COPY . /apps/CustomAppName
RUN mkdir /anvil-data

RUN useradd anvil
RUN chown -R anvil:anvil /anvil-data
USER anvil

EXPOSE 3030

ENTRYPOINT ["anvil-app-server", "--data-dir", "/anvil-data", "--origin", "https://dashboard.folivoraenergy.com", "--port", "3030", "--disable-tls", "--uplink-key", "server_E2AOUAC6U2ER5U47Y75ALWCO-ZMUP2XV7DAMOLD3F"]
CMD ["--app", "CustomAppName"]

# start uplink script
# CMD ["python3", "./functions.py"]
