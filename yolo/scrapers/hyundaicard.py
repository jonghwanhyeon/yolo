import re

from playwright.async_api import Page
from stopwatch import profile

from yolo.config import config
from yolo.logger import logger
from yolo.scrapers.scraper import Scraper, Statement
from yolo.tricker import Tricker
from yolo.utils import only_digits


class HyundaiCardScraper(Scraper):
    @staticmethod
    def should_log(url: str) -> bool:
        if re.search(r"\.(properties|woff2|woff|css|js|png|jpg|svg)\b", url) is not None:
            return False

        if re.search(r"^https?://(www\.)?hyundaicard\.com", url) is None:
            return False

        return True

    @profile(format=config.profile_format, report_at_exit=False, logger=logger)
    async def scrap(self) -> Statement:
        async with self.page_for_device("Desktop Safari") as page:
            await self._login(page)

            await page.goto("https://www.hyundaicard.com/cpa/ma/CPAMA0101_01.hc", wait_until="networkidle")

            statements = await page.locator(".items p[class^='pay']").all_text_contents()
            return Statement(spending=sum(int(only_digits(amount)) for amount in statements))

    @profile(format=config.profile_format, report_at_exit=False, logger=logger)
    async def _login(self, page: Page):
        await page.goto("https://www.hyundaicard.com/cpm/mb/CPMMB0101_01.hc")

        await page.locator("[href='#loginMethod3']").click()
        await page.locator("#webMbrId").fill(self._credential.id)

        tricker = Tricker(page)
        await page.locator("#webPwd").click()
        await tricker.fill(self._credential.password)
        await tricker.press("enter")

        await page.locator("#loginBtn").click()
        await page.wait_for_url("**/{index.jsp,CPMMB0101_02.hc}")
