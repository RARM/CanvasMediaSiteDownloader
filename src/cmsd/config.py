import logging
import os
import json

logger = logging.getLogger(__name__)

class DownloadConfiguration:
  """
  Class to manage the configuration of a download task.

  Attributes:
    file_path (str): Location of the file for this configuration.
    data (dict): Data contained for this download.
  """
  
  def __init__(self, path: str):
    """
    Initialize the DownloadConfiguration class by load or creating an empty
    configuration file.

    Args:
      path: Path to the directory of the download.
    """
    logger.debug('created new DownloadConfiguration instance')
    self.file_path = os.path.join(path, 'config.json')
    exists = os.path.exists(self.file_path)
    self.data = dict()
    if exists:
      logger.info('configuration file found')
      file = open(self.file_path, 'r')
      self.data = json.load(file)
      file.close()
    else:
      logger.debug('creating configuration file "config.json"')
      file = open(self.file_path, 'w')
      file.write('{}')
      file.close()
      