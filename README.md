# Cover-My-Resume

## TODO

add an about page

add a bug tracker

display the users username to show which account they are using

email verification: email should thank the user for creating an account with us

## If it ain't broke don't fix it section

the user input isn't being concatinated with a '+' character

## SETUP

```,
To test scraper on your machine you MUST use poetry, first create a superuser:

$ pip install poetry

$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py createsuperuser

Must export you SCRAPFLY_KEY:

$ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"

This next command will start the scraper:

$ poetry run python web_app/scrapers/indeed_scraper/run.py --job_description "Python Developer" --location "Seattle" --user_id "1"

If you get an error about a PYTHONPATH use this next command:

$ export PYTHONPATH=/your/project/level_root/cover-me-resume:$PYTHONPATH

###############################

TO RUN THE WEBSITE

You must use 3 terminals. NOTE: this project uses Google Cloud Services, this happens to me so it might happen to you but it might not, when you activate terminal 1 and 3 you might get an error about a GC_CREDENTIALS, if this is the case you must export the GCS env variables:

$ export DEFAULT_FILE_STORAGE=''

$ export GS_BUCKET_NAME=''

$ export GS_CREDENTIALS=''

$ export GS_PROJECT_ID=''

and for good measures:

$ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"

Terminal 1: 

$ python manage.py runserver

Terminal 2:

$ redis-server

Terminal 3:

$ celery -A cover_me worker --loglevel=info
```

## Making changes and deploying to production

1. Make any necessary changes

2. add and commit the changes

3. push the changes to github

4. push the changes to heroku using this command:

5. $ git push heroku main

## DONE

DONE: Deploy :D

DONE: Styling: Add CSS and JavaScript to enhance the look and user experience of your website. Consider using frontend frameworks/libraries like Bootstrap, or React

KINDA DONE: Tests: test to ensure the functionality of site. Django's built-in testing framework can be very helpful.

DONE: add a results button to the nav

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

DONE: BEFORE DEPLOYMENT: add media files that user inputs be handled by a web server or cloud storage service. web server - Nginx or service - Amazon S3 or Google Cloud

DONE: change so that the user can only have one resume, new upload overwrites the old resume

DONE: when editing the cover letter, have an option to name the cover letter file, default it to Cover_Letter

DONE: add an edit button to the cover letter in the profile page

DONE: when redownloading the cover letter, the name should be the same as it is displayed in the profile

DONE: Don't have an Upload Resume section in the nav, just put the resume upload in the home page

DONE: error with generating a cover letter

DONE: multiple resumes can now be added, change back to only have one resume

DONE: make sure job search is specific to each user

DONE: Make sure company overview link works

DONE: fix generate cover letter button
