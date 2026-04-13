import logging

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

class Scrapper:
  def __init__(self, login_url: str = None):
    logger.debug('creating Scrapper instance')
    if login_url:
      self.login_url = login_url
    else:
      self.login_url = None
    
    headless        = False if login_url else True
    self.playwright = sync_playwright().start()
    self.browser    = self.playwright.chromium.launch(headless=headless)
    self.page       = self.browser.new_page()

  def __del__(self):
    logger.debug('deleting Scrapper instance')
    self.playwright.stop()
  
  def __login(self):
    logger.debug(f'starting login routine; go to {self.login_url}')
    self.page.goto(self.login_url)
    self.page.pause()

  def get_lecture_m3u8(self, lecture_url: str = None) -> list[str]:
    # 1. Start requests tracker.
    network_url_requests = []
    # Save only files that start with "manifest".
    self.page.on('request', lambda request:
      network_url_requests.append(request.url)
      if request.url.split('/')[-1].startswith('manifest') 
      else None
    )
    # 2. Complete any login if needed or navigate to lecture.
    if self.login_url:
      self.__login()
    else:
      self.page.goto(lecture_url)
    # 3. Wait for iframe to load and videos to load.
    frame = self.page.frame_locator('#player-iframe')
    frame.locator('#vjs_video_3').wait_for()
    video_banner = frame.locator('#vjs_video_3')
    video_banner.click()
    self.page.wait_for_load_state('networkidle')
    # 4. Getting title.
    title = self.page.locator('.presentation-title').inner_text()
    # 5. Return manifest files.
    return {'title': title, 'urls': network_url_requests}