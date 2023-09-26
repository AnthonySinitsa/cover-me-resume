from django.test import TestCase
from google.cloud import storage

# for this test you must $ export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
# python web_app/tests.py
def list_blobs(bucket_name):
  """Lists all the blobs in the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)

  blobs = bucket.list_blobs()

  for blob in blobs:
    print(blob.name)

# Replace 'your-bucket-name' with the name of your bucket.
list_blobs('resumes-coverletter')
