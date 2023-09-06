# Cover-My-Resume

python manage.py migrate

python manage.py createsuperuser

run: python manage.py runserver

## TODO

DONE: However I would like to add email verification later in the future...
User Registration: While Django provides built-in views for login and logout, you might want to add a user registration system so that new users can sign up. This involves creating a registration form, view, and template.

Resume Uploading: Implement a feature allowing users to upload their resumes. This will involve creating a form for file uploads, a view to handle the form submission, and updating the Resume model to store the uploaded files.

Job Scraper Integration: If your scraper is ready, integrate it so that it runs after a user uploads their resume. The scraped job postings can be stored in the JobPost model.

Display Scraped Job Postings: Create a view and template to display the scraped job postings to the user. Allow users to select which job they're interested in.

Cover Letter Generation with ChatGPT: Once a user selects a job, use the job description and the user's resume to generate a cover letter using ChatGPT. This might involve integrating with OpenAI's API or using a local ChatGPT model, depending on your setup.

Styling and User Experience: Add CSS and JavaScript to enhance the look and user experience of your website. Consider using frontend frameworks/libraries like Bootstrap, React, or Vue.js if you're familiar with them.

Tests: Write tests to ensure the functionality of your site. Django's built-in testing framework can be very helpful.

Deployment: Once you're satisfied with your site in the development environment, plan for deployment to a live server.
