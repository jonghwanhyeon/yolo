import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from yolo.utils import is_production

root_path = Path(__file__).parent.parent.absolute()

assets_path = root_path / "assets"

if is_production():
    credentials_path = Path("/credentials")
else:
    credentials_path = root_path / "credentials"


class Credential(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    password: str


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    profile_format: str = (
        "<bold>[<blue>{module}</blue>:<green>{name}</green>]</bold>" " ~ " "<magenta>{elapsed}</magenta>"
    )

    @property
    def credentials(self) -> dict[str, Credential]:
        return {
            credential_path.stem: Credential(**json.loads(credential_path.read_text("utf-8")))
            for credential_path in credentials_path.glob("*.json")
        }


config = Config()
