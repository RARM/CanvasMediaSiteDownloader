import logging
import os

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