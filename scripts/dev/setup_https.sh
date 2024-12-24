#!/bin/bash

# For macOS, we'll use a different way to get the local IP
LOCAL_IP=$(ipconfig getifaddr en0)

# Create config file for SANs
cat > certs/openssl.cnf << EOF
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = localhost

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = ${LOCAL_IP}
EOF

# Rest of your original script...
CERT_FILE="certs/localhost.crt"
KEY_FILE="certs/localhost.key"
CSR_FILE="certs/localhost.csr"

mkdir -p certs

echo "Generating private key..."
openssl genrsa -out $KEY_FILE 2048

echo "Creating certificate signing request (CSR)..."
openssl req -new -key $KEY_FILE -out $CSR_FILE -config certs/openssl.cnf

echo "Generating self-signed certificate..."
openssl x509 -req -days 365 -in $CSR_FILE -signkey $KEY_FILE -out $CERT_FILE -extensions v3_req -extfile certs/openssl.cnf

rm -f $CSR_FILE

if ! pip show django-sslserver > /dev/null; then
    echo "Installing django-sslserver..."
    pip install django-sslserver
else
    echo "django-sslserver is already installed."
fi

# Instructions for the user
echo ""
echo "Setup complete!"
echo "Add 'sslserver' to INSTALLED_APPS in your Django project."
echo "Run the following command to start your development server with HTTPS:"
echo ""
echo "python manage.py runsslserver 127.0.0.1:8000 --certificate $CERT_FILE --key $KEY_FILE"
echo ""
# chmod +x scripts/dev/setup_https.sh
# ./scripts/dev/setup_https.sh
