#!/bin/sh
echo "-----> Installing wkhtmltopdf"

# Download wkhtmltopdf package
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Install wkhtmltopdf package
dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb || true

# Move binaries to the bin directory
mv /usr/local/bin/wkhtmltopdf /app/bin
mv /usr/local/bin/wkhtmltoimage /app/bin

echo "-----> wkhtmltopdf Installation done"
