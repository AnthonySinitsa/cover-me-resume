#!/bin/sh

WKHTMLTOPDF_VERSION='0.12.6.1-2'
WKHTMLTOPDF_DEB="wkhtmltox_${WKHTMLTOPDF_VERSION}.jammy_amd64.deb"
WKHTMLTOPDF_URL="https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOPDF_VERSION}/${WKHTMLTOPDF_DEB}"

echo "Installing wkhtmltopdf..."
curl -L $WKHTMLTOPDF_URL -o $WKHTMLTOPDF_DEB
dpkg -i $WKHTMLTOPDF_DEB
apt install -f -y
rm $WKHTMLTOPDF_DEB
