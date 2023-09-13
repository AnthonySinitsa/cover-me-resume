from celery import shared_task
import subprocess
from django.conf import settings

@shared_task
def run_scraper(job_title, job_location):
  # Set environment variables
  commands = [
    f"export SCRAPFLY_KEY='{settings.SCRAPFLY_KEY}'",
    f"export PYTHONPATH=/home/anton/projects/cover-me-resume:$PYTHONPATH",
    "poetry run python web_app/scrapers/indeed_scraper/run.py"
  ]

  # Join the commands with '&&' to run them consecutively
  command = ' && '.join(commands)

  # Use subprocess to execute the command
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()

  if process.returncode != 0:
    raise Exception(f"Scraper failed with error: {stderr.decode('utf-8')}")

  return stdout.decode('utf-8')


# project_root = Path(__file__).resolve().parents[3]  # Adjust the number based on your directory structure

#     # Define the commands to run the scraper
#     commands = [
#         f"export SCRAPFLY_KEY='{settings.SCRAPFLY_KEY}'",
#         f"export PYTHONPATH={project_root}:$PYTHONPATH",
#         "poetry run python web_app/scrapers/indeed_scraper/run.py"
#     ]