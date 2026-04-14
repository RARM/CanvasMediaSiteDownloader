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
  videos: list[URLItem]

def download_videos_set(
    videos: VideoData,
    outdir: str,
    callback: typing.Callable[[str, str, str], None] = None
  ) -> None:
  """
  Function that communicates with yt-dlp to download the videos using the
  manifest files. It downloads the files in the specified location and renames
  the files with the videos['videos']['label'] and videos['title'] values.

  You can provide a callback function that receives the label, the url, and the
  path where that video was saved.

  Args:
    videos (VideoData): Object with lecture's title and list of urls.
    outdir (str): Absolute path of folder where to save the files.
    callback (typing.Callable): Function to call after each video saved.
  """
  yt_dlp_options = {}
  for video in videos['videos']:
    # 1. Fix the name of the output directory.
    dir_title    = videos['title'].replace('/', '_').replace(':', '_')
    video_outdir = os.path.join(outdir, dir_title)
    video_outdir = get_destination_dir(video_outdir)
    # 2. Prepare the name of the output video.
    output_video_name = f'{video_outdir}/{video['label']}.mp4'
    yt_dlp_options['outtmpl'] = output_video_name
    with YoutubeDL(yt_dlp_options) as dl:
      logger.debug(f'downloading url: {video['url']}')
      dl.download(video['url'])
    # 3. Invoke callback if exists.
    if callback:
      logger.debug('callback function detected; calling')
      callback(video['label'], video['url'], output_video_name)