FROM odoo:19.0

LABEL MAINTAINER Elmer Cruz <elmerjc@gmail.com>
USER root

# Instalar dependencias adicionales del sistema
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    fonts-noto-color-emoji \
    fonts-noto-core \
    fonts-freefont-ttf \
    fonts-symbola \
    gsfonts \
    git \
    curl \
    vim \
    htop \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Ejecutar para limpiar la cache de fuentes fc-cache -f -v

# Copiar addons
COPY ./addons /mnt/extra-addons

# Copiar addons personalizados
COPY ./custom-addons /mnt/custom-addons

# Copiar configuración personalizada
COPY ./config/odoo.conf /etc/odoo/odoo.conf

RUN mkdir /usr/share/GeoIP
ADD https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb /usr/share/GeoIP/GeoLite2-City.mmdb

# Avoid externally managed environment error (PEP 668)
ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN pip3 install --upgrade setuptools && \
    pip3 install signxml==2.10.1 \
    odoorpc \
    xlsxwriter==3.0.5 \
    pandas \
    numpy \
    xlrd==2.0.1 \
    openpyxl==3.1.2 \
    gTTS==2.5.1 \
    sqlparse \
    boto3 \
    pyncclient \
    paramiko \
    gdown \
    google-auth==2.29.0
