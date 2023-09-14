# Cover-My-Resume

python manage.py migrate

python manage.py createsuperuser

run: python manage.py runserver

## TODO

DONE: User Registration, However I would like to add email verification later in the future...

DONE: Resume Uploader: for the most part finished, just need add resume to database

DONE: Add a profile page that will display all the resumes user has entered

DONE: Job Scraper Integration: If your scraper is ready, integrate it so that it runs after a user uploads their resume. The scraped job postings can be stored in the JobPost model.

DONE: Display Scraped Job Postings: Create a view and template to display the scraped job postings to the user. Allow users to select which job they're interested in.

DONE: Cover Letter Generation with ChatGPT: Once a user selects a job, use the job description and the user's resume to generate a cover letter using ChatGPT. This might involve integrating with OpenAI's API or using a local ChatGPT model, depending on your setup.

DONE: Add to profile page to show all the cover letters generated

DONE: Add a page for user to enter job and location to start the scraper

When running the scraper it shouldn't take you immediately to the results page as it will display the previous results

Add loading screen/bar till the scraper finishes

Add option to delete account

before deployment, make sure add media files that the user inputs be handled by a web server or cloud storage service. web server - Nginx or service - Amazon S3

Styling and User Experience: Add CSS and JavaScript to enhance the look and user experience of your website. Consider using frontend frameworks/libraries like Bootstrap, React, or Vue.js if you're familiar with them.

Tests: Write tests to ensure the functionality of your site. Django's built-in testing framework can be very helpful.

Deployment: Once you're satisfied with your site in the development environment, plan for deployment to a live server.

```,
This project MUST use poetry, 

COMMANDS:

$ poetry shell
  ^ starts environment (make sure to turn off .venv if installed)

$ exit
  ^ deactivate

$ redis-server
  ^ starts redis server at localhost:6379
    ^ run the server on a console and then open up another console to 
  run ↓ this command in a new console
$ celery -A cover_me worker --loglevel=info
  ^ starts the celery worker
```
