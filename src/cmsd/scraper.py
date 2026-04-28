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

  def __start_tracking_requests(self, network_url_requests: list) -> None:
    """
    This function adds a listener that saves network requests, specifically the
    m3u8 manifest requests to the `network_url_requests` parameter passed as an
    argument.

    Args:
      network_url_requests (lists): The list to update as new requests come in.
    """
    # Save only files that start with "manifest".
    self.page.on('request', lambda request:
      network_url_requests.append(request.url)
      if request.url.split('/')[-1].startswith('manifest')
      else None
    )
    logger.debug('started network requests tracking')

  def get_lecture_m3u8(self, lecture_url: str = None) -> list[str]:
    """
    Routine to retrieve m3u8 files from a lecture page in MediaSite.

    Args:
      lecture_url (str):
    """
    # 1. Start requests tracker.
    network_url_requests = []
    self.__start_tracking_requests(network_url_requests)
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

  def __get_url_of_lectures(self) -> list[str]:
    """
    This routine must be called after the `self.page` is in one of the pages of
    the catalog. It will detect and navigate to the other pages of the catalog,
    recording the URL of the lectures available.

    Return:
      list(str): The list containing the full URLs as strings.
    """
    # Get the catalog ID.
    # https://fau.mediasite.com/Mediasite/Channel/<catalog_id>/browse/null/most-recent/null/0/null
    url = self.page.url
    up = url.split('/') # url parts
    catalog_id = up[up.index('Channel') + 1] # Find the index of the "Channel" item.
    logger.debug(f'catalod ID found: {catalog_id}')
    # Get all the catalog pages.
    catalog_pages = []
    pages = self.page.locator('li.page-item.page-number a.page-link').all()
    for page in pages:
      url = page.get_attribute('href')
      if url is not None:
        catalog_pages.append(url)
    logger.debug(f'a total of {len(pages)} pages found')
    # Get the id of all lectures.
    lectures_ids = []
    for page in catalog_pages:
      self.page.goto(page)
      thumbnails = self.page.locator('.thumbnail-img-container img').all()
      for thumb in thumbnails:
        source = thumb.get_attribute('src')
        # https://fau.mediasite.com/Mediasite/FileServer/Presentation/<lecture_id>/<image_filename>.jpg?authticket=<ticket_id>
        if not source: continue
        up = url.split('/') # url parts
        lectures_ids.append(up[up.index('Presentation') + 1])
    logger.debug(f'a total of {len(lectures_ids)} lectures found')
    # Finally, build the list with all the lecture IDs.
    # https://fau.mediasite.com/Mediasite/Channel/<channel_id>/watch/<lecture_id>?sortBy=most-recent
    lectures_urls = []
    for lecture_id in lectures_ids:
      lectures_urls.append(
        f'https://fau.mediasite.com/Mediasite/Channel/{catalog_id}/watch/{lecture_id}'
      )
    logger.debug(f'a total of {len(lectures_urls)} URLs generated')
    return lectures_urls

  def get_lecture_m3u8_from_catalog(self, catalog_url: str = None) -> None:
    """
    This method retrieves m3u8 files from a MediaSite catalog.

    Args:
      catalog_url (str): MediaSite catalog URL.
    """
    # 1. Complete any login if needed or navigate to lecture.
    if self.login_url:
      self.__login()
    else:
      # FIXME: Logic for un-logged extraction may not be compatible.
      self.page.goto(catalog_url)
      time.sleep(3)
    # User must be in catalog at this point.
    lectures_urls = self.__get_url_of_lectures()

# NOTE: For future implementation of the catalog, using
# document.querySelectorAll('.watch-link') gets all the clickable lecture
# links.