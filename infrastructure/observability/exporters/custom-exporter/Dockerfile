FROM python:3.10
SHELL ["/bin/bash", "-c"]

# INSTALL ODBC Driver 17 for SQL Server - Necessary for Synapse Queries
RUN apt-get update \
    && apt-get install -y curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev \
    && apt-get clean

# Azure CLI - Necessary for Synapse Connection
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

COPY requirements.txt .

COPY /app .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["app/python", "exporter.py"]