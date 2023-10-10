#!/bin/bash

WKHTMLTOPDF_URL="https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb"

echo "-----> Installing wkhtmltopdf"
curl -L $WKHTMLTOPDF_URL -o wkhtmltopdf.deb
sudo dpkg -i wkhtmltopdf.deb
