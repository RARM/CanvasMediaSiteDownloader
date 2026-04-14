import logging
import time

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

class Scraper:
  """
  Class to manage extracting URLs from a browser. Recall the video extraction
  happnes from the user end.
  """

  def __init__(self, login_url: str = None):
    """
    Initilize a Scraper object. If a login URL is provided, a subsequent call
    will startup a browser and let the user login. Then, the user must navigate
    to the page of the lecture or the catalog to extract the videos from.

    Args:
      login_url (str): Login URL.
    """
    logger.debug('creating Scraper instance')
    headless = True
    if login_url:
      logger.debug('login_url detected; setting headless=False')
      headless = False
      self.login_url = login_url
    else:
      self.login_url = None

    self.playwright = sync_playwright().start()
    self.browser    = self.playwright.chromium.launch(headless=headless)
    self.page       = self.browser.new_page()

  def cleanup(self): # __del__ does not trigger when expected
    """
    Attempts cleans up playwright object.
    """
    logger.debug('cleaning up Scraper instance')
    self.playwright.stop()

  def __login(self):
    """
    Private function to start the login routine.
    """
    logger.debug('start login routine; login and navigate to catalog/lecture')
    self.page.goto(self.login_url)
    self.page.pause()
    logger.debug('terminating login and catalog/lecture selection routine')

  def __clean_manifests_list(self, urls: list[str]) -> list[str]:
    """
    Usually, there are two main videos to extract from MediaSite. One is the
    screen shared during class, and the other one is the classroom camera. This
    function takes the list of m3u8 files and selects the relevant ones,
    labeling them as 'main' and 'lecturer', respectively.

    Args:
      urls (list[str]): List of URL strings.

    Return:
      list: List of objects with 'label' and 'url' keys.
    """
    logger.debug(f'__clean_manifests_list called with list len {len(urls)}.')
    # 1. Get the main video.
    main = next(
      (
        url for url in urls if
        url.split('/')[-1].startswith('manifest(format=m3u8-aapl-isoff')
      ),
      None
    )
    logger.debug(f'main video url found: {main}')
    lecturer = next(
      (
        url for url in urls if
        url.split('/')[-1].startswith('manifest(video=avc1_640x360')
      ),
      None
    )
    logger.debug(f'lecturer video url found: {lecturer}')
    # 2. Package and return.
    return [
      {'label': 'main', 'url': main},
      {'label': 'lecturer', 'url': lecturer}
    ]

  def get_lecture_m3u8(self, lecture_url: str = None) -> list[str]:
    """
    Routine to retrieve m3u8 files from a lecture page in MediaSite.

    Args:
      lecture_url (str):
    """
    # 1. Start requests tracker.
    network_url_requests = []
    # Save only files that start with "manifest".
    self.page.on('request', lambda request:
      network_url_requests.append(request.url)
      if request.url.split('/')[-1].startswith('manifest')
      else None
    )
    logger.debug('started network requests tracking')
    # 2. Complete any login if needed or navigate to lecture.
    if self.login_url:
      self.__login()
    else:
      # FIXME: Logic for un-logged extraction may not be compatible.
      self.page.goto(lecture_url)
      time.sleep(3)
    # 3. Wait for iframe to load and videos to load.
    logger.debug('attempting to start player and track requests')
    frame = self.page.frame_locator('#player-iframe')
    frame.locator('.vjs-poster').wait_for() # This may be removable.
    video_poster = frame.locator('.vjs-poster')
    video_poster.click()
    time.sleep(10) # FIXME: Need a way to check the resources have loaded.
    # 4. Getting title.
    title = self.page.locator('.presentation-title').inner_text()
    logger.debug(f'lecture title retrieved: {title}')
    # 5. Return manifest urls.
    manifests_list = self.__clean_manifests_list(network_url_requests)
    return {'title': title, 'videos': manifests_list}

  def get_lecture_m3u8_from_catalog(self, catalog_url: str = None) -> None:
    """
    This method retrieves m3u8 files from a MediaSite catalog.

    Args:
      catalog_url (str): MediaSite catalog URL.
    """
    pass

# NOTE: For future implementation of the catalog, using
# document.querySelectorAll('.watch-link') gets all the clickable lecture
# links.