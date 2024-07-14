from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from yolo.config import config
from yolo.exceptions import YoloException
from yolo.logger import configure_logger, logger
from yolo.scrapers import HyundaiCardScraper, Statement

configure_logger()

scrapers = {
    "hyundaicard": HyundaiCardScraper,
}

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError) -> JSONResponse:
    error = exception.errors()[0]

    message = error["msg"]
    if ("ctx" in error) and ("error" in error["ctx"]):
        message = str(error["ctx"]["error"])

    logger.error(f"Validation error: type={error['type']}, location={error['loc']}, message={message}")
    return JSONResponse(
        content={
            "message": "An error occurred while validating the request",
            "detail": {
                "type": error["type"],
                "location": error["loc"],
                "message": message,
            },
        },
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(YoloException)
async def brain_exception_handler(request: Request, exception: YoloException) -> JSONResponse:
    logger.error(str(exception))
    return JSONResponse(
        content={"message": exception.message},
        status_code=exception.status_code,
    )


@app.get("/spending/{company}")
async def scrap_statement(company: str) -> Statement:
    if company not in scrapers:
        raise YoloException(f"Unknown company {company}")

    credential = config.credentials[company]
    scraper = scrapers[company](credential)
    return await scraper.scrap()
