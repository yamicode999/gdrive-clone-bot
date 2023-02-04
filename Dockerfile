# COMPILE
FROM python:3.10-slim-bullseye as compiler
ENV PYTHONUNBUFFERED 1

WORKDIR /project/

RUN python3 -m venv --upgrade-deps /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --no-cache-dir -U wheel \
    && pip3 install --no-cache-dir -Ur requirements.txt

# RUN
FROM python:3.10-slim-bullseye as runner

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN DEBIAN_FRONTEND="noninteractive" \
    apt-get -y update \
    && apt-get -y --no-install-recommends install \
    curl \
    git \
    procps \
    && apt-get -y clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /project/
RUN chmod 777 /project/

COPY --from=compiler /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

ENTRYPOINT ["/tini", "--"]
CMD ["bash", "start.sh"]