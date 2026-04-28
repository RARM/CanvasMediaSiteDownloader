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
    single_video: bool = False,
    config_only: bool = False
  ) -> None:
  # 1. Get and check destination.
  abs_path = get_destination_dir(destination)
  # 2. Retrieve metadata file.
  conf = DownloadConfiguration(abs_path)
  # 3. Start scraper instance.
  scraper = Scraper(download_url) if login_url else Scraper()
  videos = []
  # 5. Get list of videos (use scraper).
  if single_video:
    videos.append(scraper.get_lecture_m3u8(download_url))
    conf.update_lecture(videos[0])
  else: # Handle catalog (standard mode).
    videos = scraper.get_lecture_m3u8_from_catalog(download_url)
    conf.update_lectures(videos)
  scraper.cleanup() # Can't use the object after this.
  # 6. Download retrieved videos.
  if config_only: return
  for video in videos:
    download_videos_set(video, abs_path)
    # FIXME: Log path of the lectures in the config.
    # conf.update_lecture_filename
  return