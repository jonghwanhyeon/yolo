import json
from typing import Literal

from playwright.async_api import Locator, Page

from yolo.config import assets_path

keymap_path = assets_path / "keymap.json"

_keymap = json.loads(keymap_path.read_text("utf-8"))


class Tricker:
    def __init__(self, page: Page, event: Literal["click", "tap"] = "click"):
        self._page = page
        self._event = event

    async def fill(self, text: str):
        for character in text:
            await self.press(character)

    async def press(self, key: str):
        if key not in _keymap:
            raise ValueError(f"{key} is not a valid key")

        selector = ".kpd-group.{category} img[aria-label='{label}']".format(**_keymap[key])
        handler = getattr(self, f"_{self._event}")
        await handler(self._page.locator(selector).first)

    async def _click(self, locator: Locator):
        await locator.dispatch_event("click")

    async def _tap(self, locator: Locator):
        await locator.dispatch_event("touchstart")
        await locator.dispatch_event("touchend")
