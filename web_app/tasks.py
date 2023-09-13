from celery import shared_task
import subprocess
import os

@shared_task
def run_scraper(job_title, job_location):
  # Set environment variables
  os.environ["SCRAPFLY_KEY"] = "your_key_here"
  os.environ["PYTHONPATH"] = "/home/anton/projects/cover-me-resume"

  # Define the command to run the scraper
  cmd = ["poetry", "run", "python", "web_app/scrapers/indeed_scraper/run.py"]

  # Execute the command
  try:
    subprocess.check_call(cmd)
    # You can add more logic here to handle the output if needed.
    return "Scraper ran successfully!"
  except subprocess.CalledProcessError as e:
    # Handle errors related to the subprocess call
    return f"Scraper failed with error: {e}"
