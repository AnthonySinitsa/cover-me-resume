# THIS FILE ISN't USED BUT MIGHT NEED FOR LATER
import re

def strip_html_tags(text):
  clean = re.compile('<.*?>')
  return re.sub(clean, '', text)

def replace_paragraph_tags(text):
  text = text.replace('<p>', '\n\n').replace('</p>', '')
  return strip_html_tags(text)
