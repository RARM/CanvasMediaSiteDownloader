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
  
  def __write_attribute(self, attribute: str, value: any) -> None:
    """
    Private method to write new (or update) attributes in the config file.

    Args:
      attribute (str): Key of the attribute.
      value (any): Value of the pair.
    """
    with open(self.file_path, 'w') as file:
      self.data[attribute] = value
      json.dump(self.data, file)

  def setDownloadURL(self, url: str) -> None:
    """
    Write the download URL in the config file.

    Args:
      url (str): The download URL.
    """
    self.__write_attribute('download_url', url)

  def getDownloadURL(self) -> str:
    """
    Get the configured download URL.

    Returns:
      str: Download URL.
    """
    return self.data['download_url']