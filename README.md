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

WIP: Add a page for user to enter job and location to start the scraper

1. Create a Celery Task for the Scraper:

1. Define a new task in your Django project that will run the scraper. This task will be responsible for executing the scraper based on the provided job title and location.
You'll utilize Python's subprocess module to run the console commands for the scraper from within the task.
Modify the Django View/Endpoint:

1. Adjust the view or API endpoint where users submit the job title and location. Instead of directly running the scraper, this endpoint will queue the scraper task to be executed by a Celery worker.
Once the task is queued, you can immediately send a response back to the user, informing them that the job has started and they will be notified upon completion.
Handle Scraper Results:

1. Decide how you want to handle the results from the scraper. For instance, you might store the results in a database, create a notification for the user, or even send an email with the results.
1. Ensure error handling is robust. If the scraper fails for any reason, you should have mechanisms in place to handle such failures, possibly retrying the task or notifying an administrator.
User Notifications:

1. Consider how you want to notify users once the scraping is complete. Some options include:
Email Notifications: Send users an email when the scraper finishes with the results or a link to view the results.
Web Notifications: Use Django's messaging framework or WebSockets (e.g., Django Channels) to notify users in real-time when the scraping job completes.
Status Page: Provide a page on your website where users can check the status of their scraping jobs.
Start Celery Worker and Monitor:

1. Ensure that the Celery worker is running and ready to pick up tasks from the queue.
You can also consider setting up Celery Flower, a web-based tool for monitoring and administrating Celery clusters.
Test the Entire Workflow:

1. With everything set up, test the entire workflow from submitting a job title and location on your website to receiving the results. Ensure that tasks are correctly queued, executed by Celery workers, and that users are notified upon completion.
Optimization and Scaling (if needed):

1. If you anticipate a high volume of scraping tasks, consider scaling your Celery workers. You can run multiple workers on different machines to handle a larger number of tasks concurrently.
Monitor the memory and CPU usage to ensure that your infrastructure can handle the load.

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
