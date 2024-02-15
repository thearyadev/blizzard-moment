from PIL import Image
from PIL.Image import Image as ImageType
from typing import Final
from uuid import uuid4
from pathlib import Path



ROW_HEIGHT_PX: Final[int] = 46
ROW_SKIP_PX: Final[int] = 13
COLUMN_WIDTH_PX: Final[int] = 100
COLUMN_SKIP_PX: Final[int] = 2


def crop_to_hero_section(pil_image: ImageType) -> ImageType:
    return pil_image.crop((1392, 294, 1696, 871))


def crop_split_row(pil_image: ImageType) -> list[ImageType]:
    current_offset_pos: int = 0
    o_width, o_height = pil_image.size
    result: list[ImageType] = list()
    for _ in range(10):
        result.append(
            pil_image.copy().crop(
                (
                    0,
                    current_offset_pos,
                    o_width,
                    min(current_offset_pos + ROW_HEIGHT_PX, o_height),
                )
            )
        )
        current_offset_pos += ROW_HEIGHT_PX + ROW_SKIP_PX
        if current_offset_pos >= o_height:
            break

    return result


def crop_split_column(pil_image: ImageType) -> list[ImageType]:
    current_offset_pos: int = 0
    result: list[ImageType] = list()
    o_width, o_height = pil_image.size
    for _ in range(3):
        result.append(
            pil_image.copy().crop(
                (
                    current_offset_pos,
                    0,
                    min(current_offset_pos + COLUMN_WIDTH_PX, o_width),
                    o_height
                )
            )
        )
        current_offset_pos += COLUMN_WIDTH_PX + COLUMN_SKIP_PX
        if current_offset_pos >= o_width:
            break
    return list(reversed(result)) # Hero placement has been reversed in Season 9 (blizzard moment.)


if __name__ == "__main__":
    for f in Path("./lb").iterdir():
        imgs = crop_split_row(crop_to_hero_section(Image.open("./man.png")))
        for img in imgs:
            for i in crop_split_column(img):
                i.save("./tmp2/" + uuid4().hex + ".png")
        break