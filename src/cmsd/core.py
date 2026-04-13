from .config import DownloadConfiguration
from .utils import get_destination_dir

import logging

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def downloader(
    media_site_page_url: str,
    destination: str,
    login_url: str = None,
  ):
  # 1. Get and check destination.
  abs_path = get_destination_dir(destination)
  # 2. Retrieve for metadata file.
  conf = DownloadConfiguration(abs_path)
  # 3. Retrieve video urls.
  # 4. Download videos.
  return

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