from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from playwright.async_api import Page, Request, Response, async_playwright
from pydantic import BaseModel
from tml import markup

from yolo.config import Credential
from yolo.logger import logger


class Statement(BaseModel):
    spending: int


class Scraper(ABC):
    def __init__(self, credential: Credential):
        self._credential = credential

    @staticmethod
    @abstractmethod
    def should_log(url: str) -> bool: ...

    @abstractmethod
    async def scrap(self, page: Page) -> Statement: ...

    @asynccontextmanager
    async def page_for_device(self, device: str) -> AsyncGenerator[Page, None]:
        async with async_playwright() as playwright:
            browser = await playwright.webkit.launch()
            context = await browser.new_context(**playwright.devices[device])
            page = await context.new_page()

            def on_request(request: Request):
                if self.should_log(request.url):
                    logger.info(
                        markup(
                            f"<bold><blue>[{type(self).__name__}]</blue></bold>"
                            " "
                            "<bold><green>>>>></green></bold>"
                            " "
                            f"{request.url}"
                        )
                    )

            def on_response(response: Response):
                if self.should_log(response.url):
                    logger.info(
                        markup(
                            f"<bold><blue>[{type(self).__name__}]</blue></bold>"
                            " "
                            "<bold><yellow><<<<</yellow></bold>"
                            " "
                            f"{response.url}"
                        )
                    )

            page.on("request", on_request)
            page.on("response", on_response)

            yield page

            await page.close()
            await context.close()
            await browser.close()
