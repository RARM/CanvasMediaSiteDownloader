import logging
import os
import shutil

logger = logging.getLogger(__name__)

def get_destination_dir(path: str) -> str:
  """
  Utility function to return the absolute format of a path. During checking,
  this function will create it (and any intermediate directories) if it does
  not exist.

  Args:
    path (str): Relative path to process.

  Returns:
    str: Absolute path.
  """
  logger.debug(f'path received: "{path}"')
  abs_path = os.path.abspath(path)
  exists   = os.path.exists(abs_path)
  
  logger.debug(f'absolute path: "{abs_path}"')
  if not exists:
    logger.info('creating destination folder')
    os.makedirs(abs_path)
  else:
    logger.debug('destination folder found')
  
  return abs_path

def checks() -> bool:
  """
  Check whether the system has the third-party software required to run. This
  function will print an error log if the system does not meet the
  requirements.

  Returns:
    bool: True if it has all the programs required; false otherwise.
  """
  good = True
  requires = ['yt-dlp']
  for required in requires:
    if shutil.which(required):
      good = False
      logger.error(f'could not find {required}; please install program')
  return good