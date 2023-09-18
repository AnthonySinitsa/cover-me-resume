# Cover-My-Resume

## DONE

DONE: User Registration

DONE: Resume Uploader: for the most part finished, just need add resume to database

DONE: Add a profile page that will display all the resumes user has entered

DONE: Job Scraper Integration: If your scraper is ready, integrate it so that it runs after a user uploads their resume. The scraped job postings can be stored in the JobPost model.

DONE: Display Scraped Job Postings: Create a view and template to display the scraped job postings to the user. Allow users to select which job they're interested in.

DONE: Cover Letter Generation with ChatGPT: Once a user selects a job, use the job description and the user's resume to generate a cover letter using ChatGPT. This might involve integrating with OpenAI's API or using a local ChatGPT model, depending on your setup.

DONE: Add to profile page to show all the cover letters generated

DONE: Add a page for user to enter job and location to start the scraper

DONE: When running the scraper it shouldn't take you immediately to the results page as it will display the previous results

DONE: Add loading screen/bar till the scraper finishes

DONE: fix up the job-results page to have a nav bar at top

DONE: add option to delete account

## TODO

BEFORE DEPLOYMENT: add media files that user inputs be handled by a web server or cloud storage service. web server - Nginx or service - Amazon S3 or Google Cloud

email verification

can't have more than one account on same email address

Tests: test to ensure the functionality of site. Django's built-in testing framework can be very helpful.

Styling and User Experience: Add CSS and JavaScript to enhance the look and user experience of your website. Consider using frontend frameworks/libraries like Bootstrap, or React

Deploy :D

## SETUP

```,
 ***This project MUST use poetry, just get rid of stinky .venv***

COMMANDS🌈:

$ pip install poetry

$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py createsuperuser

$ python manage.py runserver
  ^ seperate terminal

$ poetry shell
  ^ starts environment ($ deactivate)

$ redis-server
  ^ seperate terminal (runs redis server)

$ celery -A cover_me worker --loglevel=info
  ^ seperate terminal (starts the celery worker)
```

```,
for this step:
Upload the key to your server: If your Django project is running on a server, you'll need to securely upload this .json file to your server.
is this assuming the website is deployed?
ChatGPT
Yes, the step to upload the key to your server assumes that your Django project is deployed on a remote server. If you're currently working on your local development machine, you can simply store the .json file in a secure location on your local system and provide the local path to it in GS_CREDENTIALS.

However, when you do deploy your Django project to a production server, you'll need to transfer the .json service account key to the server and adjust the GS_CREDENTIALS path accordingly.

Additionally, always remember:

Never commit the .json service account key to version control (like Git). It contains sensitive credentials.
When deploying, ensure that only the necessary personnel or processes can read the .json file, as it provides access to your Google Cloud Storage. This usually means setting tight file permissions on it.
```

1. Test:
Before deploying, test the file uploads locally to ensure they're being uploaded to GCS.

1. Clean-up:
Remember to adjust permissions on your GCS bucket to ensure that only the required entities can read or write to it. Avoid making it public unless necessary.

1. Going further:
You can configure the django-storages backend to use different storage classes, enable automatic file overwriting, or specify a custom location (sub-directory) within your bucket.
Consider enabling HTTPS for your bucket if you're serving user-facing content.
Regularly review and manage storage costs. GCS charges for storage space, network costs, and operations.
By following these steps, you should have your Django application storing files on GCS!

export DEFAULT_FILE_STORAGE=''
export GS_BUCKET_NAME=''
export GS_CREDENTIALS=''
export GS_PROJECT_ID=''
