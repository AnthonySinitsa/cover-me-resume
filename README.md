# Cover-My-Resume

python manage.py migrate

python manage.py createsuperuser

run: python manage.py runserver

## TODO

DONE: User Registration, However I would like to add email verification later in the future...

Resume Uploader: for the most part finished, just need add resume to database

DONE: Add a profile page that will display all the resumes user has entered

Job Scraper Integration: If your scraper is ready, integrate it so that it runs after a user uploads their resume. The scraped job postings can be stored in the JobPost model.

Display Scraped Job Postings: Create a view and template to display the scraped job postings to the user. Allow users to select which job they're interested in.

Cover Letter Generation with ChatGPT: Once a user selects a job, use the job description and the user's resume to generate a cover letter using ChatGPT. This might involve integrating with OpenAI's API or using a local ChatGPT model, depending on your setup.

Styling and User Experience: Add CSS and JavaScript to enhance the look and user experience of your website. Consider using frontend frameworks/libraries like Bootstrap, React, or Vue.js if you're familiar with them.

Tests: Write tests to ensure the functionality of your site. Django's built-in testing framework can be very helpful.

Deployment: Once you're satisfied with your site in the development environment, plan for deployment to a live server.

Add to profile page to show all the cover letters generated
