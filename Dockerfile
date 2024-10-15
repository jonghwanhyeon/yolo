FROM mcr.microsoft.com/playwright:v1.47.0-jammy
ENV PYTHONUNBUFFERED=1

RUN wget -O /tmp/get-pip.py "https://bootstrap.pypa.io/get-pip.py" \
    && python3 /tmp/get-pip.py --no-cache-dir \
    && rm /tmp/get-pip.py

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --requirement requirements.txt

COPY . .

VOLUME /credentials

EXPOSE 80
ENTRYPOINT ["./docker-entrypoint.sh"]