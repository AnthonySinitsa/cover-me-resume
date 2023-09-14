# This file specifies that the scraper should identify and retrieve job information based on each job's ID key. 

# https://github.com/scrapfly/scrapfly-scrapers/tree/main/indeed-scraper
# To run this script set the env variable $SCRAPFLY_KEY with your scrapfly API key:
# $ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
# export PYTHONPATH=/home/anton/projects/cover-me-resume:$PYTHONPATH
# poetry run python web_app/scrapers/indeed_scraper/run.py --job_description "Python Developer" --location "Seattle"


import sys
from pathlib import Path
import json
import argparse
import asyncio

sys.path.append(str(Path(__file__).parent.parent.parent))

from web_app.scrapers.indeed_scraper.indeed import BASE_CONFIG
import web_app.scrapers.indeed_scraper.indeed as indeed

output = Path(__file__).parent / "results"
output.mkdir(parents=True, exist_ok=True)

async def run(job_specification, location):
  # enable scrapfly cache for basic use
  BASE_CONFIG["cache"] = True

  url = f"https://www.indeed.com/jobs?q={job_specification}&l={location}"
  result_search = await indeed.scrape_search(url, max_results=10)
  output.joinpath("search.json").write_text(json.dumps(result_search, indent=2, ensure_ascii=False))
  
  # Extract job keys from the search results
  job_keys = [job['jobkey'] for job in result_search]
      
  # Save the extracted job keys to a list
  # job_keys_path = output.joinpath("job_keys.txt")
  # job_keys_path.write_text('\n'.join(job_keys))
  
  result_jobs = await indeed.scrape_jobs(job_keys)
  output.joinpath("jobs.json").write_text(json.dumps(result_jobs, indent=2, ensure_ascii=False))


def parse_arguments():  # <-- Add this function to parse command-line arguments
  parser = argparse.ArgumentParser(description="Indeed.com Job Scraper")
  parser.add_argument("--job_description", required=True, help="Job description to search for")
  parser.add_argument("--location", required=True, help="Location to search")
  return parser.parse_args()


if __name__ == "__main__":
  args = parse_arguments()
  job_description = args.job_description
  location = args.location
  asyncio.run(run(job_description, location))
