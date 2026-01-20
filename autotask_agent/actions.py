import uiautomator2 as u2
from loguru import logger
from typing import Optional, Tuple
import time
import os


class AndroidActions:
    """Low-level, safe Android automation actions"""

    def __init__(self, device: u2.Device):
        self.device = device
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self._ensure_screen_on()


    def _ensure_screen_on(self):
        try:
            if not self.device.info.get("screenOn", True):
                self.device.screen_on()
                time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Screen wake failed: {e}")


    def get_screen_size(self) -> Tuple[int, int]:
        info = self.device.info
        return (
            info.get("displayWidth", 1080),
            info.get("displayHeight", 1920),
        )

    def take_screenshot(self, name: Optional[str] = None) -> str:
        if not name:
            name = f"screen_{int(time.time())}.png"

        path = os.path.join(self.screenshot_dir, name)
        self.device.screenshot(path)
        logger.debug(f"Screenshot saved: {path}")
        return path


    def tap(self, x: int, y: int, retries: int = 2):
        for _ in range(retries):
            try:
                self.device.click(x, y)
                time.sleep(0.3)
                return
            except Exception:
                time.sleep(0.2)
        logger.error(f"Tap failed at ({x}, {y})")

    def swipe_percent(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        duration: float = 0.3,
    ):
        w, h = self.get_screen_size()
        self.device.swipe(
            int(w * start_x),
            int(h * start_y),
            int(w * end_x),
            int(h * end_y),
            duration,
        )
        time.sleep(0.3)

    def scroll(self, direction: str = "down"):
        if direction == "down":
            self.swipe_percent(0.5, 0.8, 0.5, 0.3)
        elif direction == "up":
            self.swipe_percent(0.5, 0.3, 0.5, 0.8)
        elif direction == "left":
            self.swipe_percent(0.8, 0.5, 0.3, 0.5)
        elif direction == "right":
            self.swipe_percent(0.3, 0.5, 0.8, 0.5)

        logger.debug(f"Scrolled {direction}")


    def input_text(self, text: str):
        try:
            self.device.clear_text()
            time.sleep(0.1)
        except Exception:
            pass

        self.device.send_keys(text)
        time.sleep(0.3)
        logger.debug(f"Input text: {text}")

    def press_enter(self):
        self.device.press("enter")
        time.sleep(0.2)


    def press_back(self):
        self.device.press("back")
        time.sleep(0.3)

    def press_home(self):
        self.device.press("home")
        time.sleep(0.5)


    def open_app(self, package_name: str):
        try:
            self.device.app_start(package_name)
            logger.info(f"Opened app: {package_name}")
            time.sleep(1.5)
        except Exception as e:
            logger.error(f"App open failed: {e}")
            raise

    def get_current_app(self) -> Optional[str]:
        try:
            info = self.device.app_current()
            return info.get("package")
        except Exception:
            return None
        

    def find_and_tap_text(self, text: str, partial: bool = True, retries: int = 2) -> bool:
        for _ in range(retries):
            try:
                element = (
                    self.device(textContains=text)
                    if partial
                    else self.device(text=text)
                )

                if element.exists:
                    element.click()
                    time.sleep(0.3)
                    logger.info(f"Tapped text: {text}")
                    return True
            except Exception:
                time.sleep(0.3)

        logger.warning(f"Text not found: {text}")
        return False

    def find_and_tap_description(self, description: str, retries: int = 2) -> bool:
        for _ in range(retries):
            try:
                element = self.device(descriptionContains=description)
                if element.exists:
                    element.click()
                    time.sleep(0.3)
                    logger.info(f"Tapped description: {description}")
                    return True
            except Exception:
                time.sleep(0.3)

        return False

    def wait_for_element(self, text: str, timeout: int = 10) -> bool:
        try:
            return self.device(textContains=text).wait(timeout=timeout)
        except Exception:
            return False


    def open_notification_bar(self):
        self.device.open_notification()
        time.sleep(0.5)

    def open_quick_settings(self):
        self.device.open_quick_settings()
        time.sleep(0.5)