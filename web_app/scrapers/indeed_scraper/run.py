# This file specifies that the scraper should identify and retrieve job information based on each job's ID key. 

# https://github.com/scrapfly/scrapfly-scrapers/tree/main/indeed-scraper
# To run this script set the env variable $SCRAPFLY_KEY with your scrapfly API key:
# $ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
# export PYTHONPATH=/home/anton/projects/cover-me-resume:$PYTHONPATH
# poetry run python web_app/scrapers/indeed_scraper/run.py --job_description "Python Developer" --location "Seattle" --user_id "1"

import os
import sys
import json
import django
import logging
import asyncio
import argparse
import psycopg2
import traceback
from pathlib import Path
from asgiref.sync import sync_to_async
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cover_me.settings')
django.setup()
from web_app.models import Job
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import transaction

sys.path.append(str(Path(__file__).parent.parent.parent))

from web_app.scrapers.indeed_scraper.indeed import BASE_CONFIG
import web_app.scrapers.indeed_scraper.indeed as indeed

output = Path(__file__).parent / "results"
output.mkdir(parents=True, exist_ok=True)


@sync_to_async
def clear_existing_jobs(user):
  Job.objects.filter(user=user).delete()
  logging.info(f'Deleted all existing jobs for user {user.id}')


@sync_to_async
def save_job_to_db(user, job, location):
  try:
    logging.info(f'Received job data: {job["companyName"]}')

    Job.objects.create(
      user=user,
      title=job['jobTitle'],
      company=job['companyName'],
      location=location,
      description=job['description'],
      post_date=timezone.now(),
      company_overview_link=job.get('companyOverviewLink', ''),
    )
    logging.info(f'Saved job to database: {job["companyName"]}')
    
  except Exception as e:
    logging.error(f'Error saving job {job["companyName"]} to database for user: {user.id}: {e}')



@sync_to_async
def get_user_by_id(user_id):
  try:
    return User.objects.get(id=user_id)
  except ObjectDoesNotExist as e:
    logging.error(f"User with id {user_id} does not exist: {e}")
  except psycopg2.OperationalError as e:
    logging.error(f"Operational error while getting the user: {e}")
    logging.error(traceback.format_exc())  # Log the full stack trace for more details
  except Exception as e:
    logging.error(f"An error occurred while getting the user: {e}")
    logging.error(traceback.format_exc())  # Log the full stack trace for more details


@transaction.atomic
async def run(job_specification, location, user_id):
  # enable scrapfly cache for basic use
  BASE_CONFIG["cache"] = True

  url = f"https://www.indeed.com/jobs?q={job_specification}&l={location}"
  result_search = await indeed.scrape_search(url, max_results=10)
  job_keys = [job['jobkey'] for job in result_search]
  result_jobs = await indeed.scrape_jobs(job_keys)

  logging.info(f'Number of jobs retrieved: {len(result_jobs)}')
  
  try:
    user = await get_user_by_id(user_id)
  except ObjectDoesNotExist as e:
    logging.error(f"User with id {user_id} does not exist: {e}")
    return
  except Exception as e:
    logging.error(f"An error occurred while getting the user: {e}")
    return

  # Clear existing jobs before saving new ones
  await clear_existing_jobs(user)

  for job in result_jobs:
    # adding safety check to handle NoneType jobs
    if job is None:
      logging.warning('Skipped job because job data is None')
      continue
    
    # Adding the skipping logic here
    if not job['jobTitle'] or not job['companyName'] or not job['description'] or not job.get('companyOverviewLink'):
      logging.warning(f"Skipped a job because of missing data: {job['companyName']}")
      continue  # Skip this iteration and proceed to the next job

    # If job data is complete, save it to the database
    await save_job_to_db(user, job, location)

  logging.info('Job data saved to database')




def parse_arguments():
  parser = argparse.ArgumentParser(description="Indeed.com Job Scraper")
  parser.add_argument("--job_description", required=True, help="Job description to search for")
  parser.add_argument("--location", required=True, help="Location to search")
  parser.add_argument("--user_id", required=True, type=int, help="User ID")
  return parser.parse_args()

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  args = parse_arguments()
  job_description = args.job_description
  location = args.location
  user_id = args.user_id
  asyncio.run(run(job_description, location, user_id))
