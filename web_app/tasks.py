import asyncio
from celery import shared_task
from web_app.scrapers.indeed_scraper.run import run as scraper_run

@shared_task
def run_scraper(job_title, job_location):
  try:
    print("Starting scraper...")  # Add this print statement
    asyncio.run(scraper_run(job_title, job_location))  # Wrap the function with asyncio.run
    print("Scraper finished successfully.")  # Add this print statement
    return "Scraper completed successfully."
  except Exception as e:
    print(f"Exception encountered: {str(e)}")  # Add this print statement
    return f"Scraper failed with error: {str(e)}"
