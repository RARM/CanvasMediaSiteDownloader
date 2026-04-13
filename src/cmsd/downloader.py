import logging
import os
import typing

from .utils import get_destination_dir

from yt_dlp import YoutubeDL

logger = logging.getLogger(__name__)

class URLItem(typing.TypedDict):
  label: str
  url: str

class VideoData(typing.TypedDict):
  title: str
  urls: list[URLItem]

def download_videos_set(videos: VideoData, outdir: str) -> None:
  """
  Function that communicates with yt-dlp to download the videos using the
  manifest files. It downloads the files in the specified location and renames
  the files with the videos['urls']['label'] and videos['title'] values.

  Args:
    videos (VideoData): Object with lecture's title and list of urls.
    outdir (str): Absolute path of folder where to save the files.
  """
  yt_dlp_options = {}
  for video in videos['urls']:
    dir_title    = videos['title'].replace('/', '_').replace(':', '_')
    video_outdir = os.path.join(outdir, dir_title)
    video_outdir = get_destination_dir(video_outdir)
    yt_dlp_options['outtmpl'] = f'{video_outdir}/{video['label']}.mp4'
    with YoutubeDL(yt_dlp_options) as dl:
      logger.debug(f'downloading url: {video['url']}')
      dl.download(video['url'])