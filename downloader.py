"""
Short description.

Longer description goes here.

Author: Rodolfo Andrés Rivas Matta
Date: 2026-04-10
"""

import argparse
import logging

from playwright.sync_api import sync_playwright

PROGRAM_NAME = 'MediaSiteDownloader'
__author__ = "Rodolfo Andrés Rivas Matta"
__version__ = "0.0.1"
logger = logging.getLogger(PROGRAM_NAME)

def save_auth(url: str) -> list[str]:
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page    = context.new_page()

    page.goto('https://canvas.fau.edu/')
    page.pause()

    context.storage_state(path='auth.json')
    logger.info('Browser context saved in "auth.json".')
    
    browser.close()
  return []

def open_protected_page():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state='auth.json')
    page    = context.new_page()

    page.goto('https://fau.mediasite.com/Mediasite/Channel/db0c83ebb09145cca8a77b39ac21afd75f/browse/null/most-recent/null/0/null')
    page.pause()

    browser.close()
  return

# ===========
# Main Driver
# ===========

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog=PROGRAM_NAME,
    description='This script can download all lectures from a MediaSite page.'
  )
  parser.add_argument('URL', help='location of the page with the lectures')
  args = parser.parse_args()

  logging.basicConfig(level=logging.INFO)

  logger.info(f'received "{args.URL}" as URL')
  open_protected_page()