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

DONE: BEFORE DEPLOYMENT: add media files that user inputs be handled by a web server or cloud storage service. web server - Nginx or service - Amazon S3 or Google Cloud

DONE: change so that the user can only have one resume, new upload overwrites the old resume

DONE: when editing the cover letter, have an option to name the cover letter file, default it to Cover_Letter

DONE: add an edit button to the cover letter in the profile page

DONE: when redownloading the cover letter, the name should be the same as it is displayed in the profile

DONE: Don't have an Upload Resume section in the nav, just put the resume upload in the home page

## TODO

error with generating a cover letter

add an about page

make sure job search is specific to each user

add a bug tracker

display the users username to show which account they are using

email verification: email should thank the user for creating an account with us

Tests: test to ensure the functionality of site. Django's built-in testing framework can be very helpful.

Styling: Add CSS and JavaScript to enhance the look and user experience of your website. Consider using frontend frameworks/libraries like Bootstrap, or React

Deploy :D

## SETUP

```,
 ***This project MUST use poetry, just get rid of stinky .venv***
 ***actualy i don't think you have to use poetry anymore***
 ***just use a venv***

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

This will get rid of the .venv visual bug

export PS1="%{%}➜ %{%}%c%{%} $(git_prompt_info)"

```,
1. Setting up the React Frontend:
New Repository: You can create a new repository for the React frontend. This keeps your frontend and backend codebases separate, which can be beneficial for development, especially if different teams are working on each part.

Create React App: Use Create React App (CRA) to set up a new React project:

bash
Copy code
npx create-react-app my-react-frontend
API Calls: Your React frontend will communicate with your Django backend using HTTP API calls. To make these calls, you can use libraries like axios or the built-in fetch API.

2. Setting up the Django Backend:
Django REST Framework: If not already set up, consider using the Django REST framework (DRF) to transform your Django application into an API that your React frontend can consume.

CORS Headers: To handle Cross-Origin Resource Sharing (CORS) and allow your React frontend to make requests to your Django backend, you'll need to install django-cors-headers:

bash
Copy code
pip install django-cors-headers
Then, add it to your INSTALLED_APPS and MIDDLEWARE in settings.py, and configure the origins that are allowed to access your backend.

3. Connecting Frontend to Backend:
Environment Variables: Use environment variables or a configuration file in your React app to store the base URL of your Django API. This way, when you switch between development, staging, and production, you can easily change the API's URL without modifying the code.

API Calls: When making API calls from your React app, use the base URL from your environment variables, followed by the specific endpoint you want to access.

4. Deployment:
Separate Deployment:

Backend: Deploy your Django application as you would normally, for instance, using a platform like Heroku, DigitalOcean, AWS, etc.
Frontend: Deploy your React application to platforms specialized for static sites, like Netlify, Vercel, or even Amazon S3.
Combined Deployment:

You can also serve your React app as static files from Django. After building your React app (npm run build), you can copy the build files to Django's static directory and serve them. This method is less common because it couples the frontend and backend deployments.
Domain Configuration:

Separate Subdomains: For example, use api.mywebsite.com for your Django backend and www.mywebsite.com for your React frontend.
Same Domain: If using the same domain, you can use a path for the API, like mywebsite.com/api/.
5. Considerations:
State Management: As your React app grows, consider using state management solutions like Redux or React Context API to manage the state of your application more efficiently.
Authentication: If you have authentication in your Django app, consider using token-based authentication (e.g., JWT) to authenticate your React app with the Django backend.
Real-time Communication: If needed, consider using technologies like WebSockets (e.g., Django Channels) for real-time features.
```
