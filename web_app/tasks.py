import asyncio
import time
from celery import shared_task
from web_app.scrapers.indeed_scraper.run import run as scraper_run

MAX_RETRIES = 5
RETRY_DELAY = 5 # time in seconds

@shared_task
def run_scraper(job_title, job_location, user_id):
  for attempt in range(MAX_RETRIES):
    try:
      print("Starting scraper...")
      asyncio.run(scraper_run(job_title, job_location, user_id))  # Wrap the function with asyncio.run
      print("Scraper finished successfully.")
      return "Scraper completed successfully."
    except Exception as e:
      print(f"Attempt {attempt + 1} failed with error: {str(e)}")
      if "ERR::ASP::SHIELD_PROTECTION_FAILED" in str(e) and attempt < MAX_RETRIES - 1:
        print(f"Retrying in {RETRY_DELAY} seconds due to anti-scraping protection...")
        time.sleep(RETRY_DELAY)
      else:
        print("Scraper failed with error:", str(e))
        return f"Scraper failed with error: {str(e)}"
