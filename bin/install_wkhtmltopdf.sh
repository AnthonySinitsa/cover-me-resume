#!/bin/sh
echo "-----> Installing wkhtmltopdf"

# Assuming the wkhtmltopdf binary is included in the project repository root
# Copy wkhtmltopdf binary to the bin directory
cp wkhtmltopdf /app/bin/
chmod +x /app/bin/wkhtmltopdf  # Make sure it is executable

echo "wkhtmltopdf installed at:"
ls -alh /app/bin/wkhtmltopdf  # This will confirm that the file is present and executable

echo "-----> wkhtmltopdf Installation done"

