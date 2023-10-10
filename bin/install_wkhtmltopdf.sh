#!/bin/sh
echo "-----> Installing wkhtmltopdf"

# Download wkhtmltopdf package
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Create a temporary directory
mkdir /app/tmp

# Extract the Debian package to the temporary directory
dpkg-deb -x wkhtmltox_0.12.6.1-2.jammy_amd64.deb /app/tmp

# Move binaries to the bin directory
mv /app/tmp/usr/local/bin/wkhtmltopdf /app/bin
mv /app/tmp/usr/local/bin/wkhtmltoimage /app/bin

# Clean up the temporary directory
rm -rf /app/tmp

echo "-----> wkhtmltopdf Installation done"
