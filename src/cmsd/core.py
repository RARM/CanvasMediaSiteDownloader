from .config import DownloadConfiguration
from .utils import get_destination_dir
from .scraper import Scraper
from .downloader import download_videos_set

import logging

logger = logging.getLogger(__name__)

def driver(
    download_url: str,
    destination: str,
    login_url: bool = False,
    single_video: bool = False
  ):
  # 1. Get and check destination.
  abs_path = get_destination_dir(destination)
  # 2. Retrieve metadata file.
  conf = DownloadConfiguration(abs_path)
  # 3. Start scraper instance.
  scraper = Scraper(download_url) if login_url else Scraper()
  videos = []
  # 5. Get list of videos (use scraper).
  if single_video and login_url:
    videos.append(scraper.get_lecture_m3u8())
    conf.appendLecture(videos[0])
  else: # Handle catalog (standard mode).
    pass
  scraper.cleanup() # Can't use the object after this.
  # 6. Download retrieved videos.
  for video in videos:
    download_videos_set(video, abs_path)
    # conf.update_lecture_filename
  return