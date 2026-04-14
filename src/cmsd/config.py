from .downloader import VideoData

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
      path (str): Path to the directory of the download.
    """
    logger.debug('created new DownloadConfiguration instance')
    self.file_path = os.path.join(path, 'config.json')
    self.exists = os.path.exists(self.file_path)
    self.data = dict()
    if self.exists:
      logger.info('configuration file found')
      file = open(self.file_path, 'r')
      self.data = json.load(file)
      file.close()
    else:
      logger.debug('creating configuration file "config.json"')
      file = open(self.file_path, 'w')
      json.dump(self.data, file)
      file.close()
  
  def is_new(self) -> bool:
    """
    Checks whether the inistantiation of this object created a new config file.

    Returns:
      bool: True if the config did not exist; false otherwise.
    """
    return not self.exists
  
  def __write_file_update(self) -> None:
    """
    Private method to write current status of the data in the config file.
    """
    logger.debug('synching config file')
    with open(self.file_path, 'w') as file:
      json.dump(self.data, file)

  def setDownloadURL(self, url: str) -> None:
    """
    Write the download URL in the config file.

    Args:
      url (str): The download URL.
    """
    self.data['download_url'] = url
    self.__write_file_update()

  def getDownloadURL(self) -> str:
    """
    Get the configured download URL.

    Returns:
      str: Download URL.
    """
    return self.data['download_url']
  
  def appendLecture(self, lecture: VideoData) -> None:
    """
    Save metadata of a video set (a lecture).

    Args:
      lecture (VideoData): Lecture object to append to the lectures attribute.
    """
    logger.debug(f'saving/updating lecture in config file: {lecture['title']}')
    # Create object if it doesn’t exist.
    if not self.data.get('lectures'):
      self.data['lectures'] = []
    # Get lecture (if it already exists).
    existing_match = next(
      (
        item for item in self.data['lectures'] if
        item.get('title') == lecture['title']
      )
      , None
    )
    if existing_match: # Update if it exists.
      logger.debug('item exists; updating values')
      existing_match.update(lecture)
    else: # Append if it does not exist.
      logger.debug('item does not exist; appending video set')
      self.data['lectures'].append(lecture)
    return self.__write_file_update()