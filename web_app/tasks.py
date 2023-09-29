import asyncio
from celery import shared_task
from web_app.scrapers.indeed_scraper.run import run as scraper_run

@shared_task
def run_scraper(job_title, job_location, user_id):
  try:
    print("Starting scraper...")
    asyncio.run(scraper_run(job_title, job_location, user_id))  # Wrap the function with asyncio.run
    print("Scraper finished successfully.")
    return "Scraper completed successfully."
  except Exception as e:
    print(f"Exception encountered: {str(e)}")
    return f"Scraper failed with error: {str(e)}"
