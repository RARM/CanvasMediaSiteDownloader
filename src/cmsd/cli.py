"""
Script to download lectures from MediaSite by Florida Atlantic University.

This script can download a multi-video lecture (where there is a video of the
speaker and another of the presentation) from MediaSite. The script is designed
for the Florida Atlantic University system.
"""

from .core import driver

import argparse
import logging

PROGRAM_NAME = 'cmsd'
__author__ = "Rodolfo Andrés Rivas Matta"
__version__ = "0.0.1"
logger = logging.getLogger(__name__)

def main():
  """
  Program entry point for the CLI.
  """
  # Configure the parser.
  parser = argparse.ArgumentParser(
    prog=PROGRAM_NAME,
    description='Script to download lectures from MediaSite by Florida' \
    ' Atlantic University.'
  )
  parser.add_argument('url', help='location of the page with the lectures')
  parser.add_argument(
    '-v', '--verbose', type=int, default=logging.DEBUG, # set to logging.INFO
    help='set the log level; 0 (very verbose) to 50 (only critical)'
  )
  parser.add_argument(
    '-d', '--destination', required=True,
    help='path to the destination folder for the download'
  )
  parser.add_argument(
    '-s', action='store_true',
    help='if set, treat url as single lecture, not the MediaSite catalog'
  )
  parser.add_argument(
    '-l', '--login-url', action='store_true',
    help='if set, use URL as login page; manually navigate to lectures'
  )
  args = parser.parse_args()

  # Configure logging.
  logging.basicConfig(level=args.verbose)

  # 1. Print passed information.
  if args.login_url:
    logger.debug(f'configured login_url={args.login_url}')
  logger.debug(f'configured url="{args.url}"')
  logger.debug(f'configured destination="{args.destination}"')
  logger.debug(f'configured verbose={args.verbose}')
  logger.debug(f'configured s={args.s}')

  # 2. Call driver.
  driver(args.url, args.destination, args.login_url, args.s)  