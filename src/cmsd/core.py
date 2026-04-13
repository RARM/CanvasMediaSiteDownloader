from .config import DownloadConfiguration
from .utils import get_destination_dir
from .scrapper import Scrapper

import logging

logger = logging.getLogger(__name__)

def downloader(
    download_url: str,
    destination: str,
    login_url: bool = False,
    single_video: bool = False
  ):
  # 1. Get and check destination.
  abs_path = get_destination_dir(destination)
  # 2. Retrieve metadata file.
  conf = DownloadConfiguration(abs_path)
  # 3. Start scrapper instance.
  scrapper = Scrapper(download_url) if login_url else Scrapper()
  videos = []
  # 5. Directly download if single video mode.
  if single_video and login_url:
    videos.append(scrapper.get_lecture_m3u8()) # Don't forget to update conf.
  # 6. Download retrieved videos.
  
  return