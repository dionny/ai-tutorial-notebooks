import io
import re
from typing import Tuple

from ipywidgets.widgets.widget_upload import FileUpload
import PIL.Image
import PIL.ImageDraw


class ErrorMessage:
    UPLOAD_ERROR = 'No image uploaded.'
    BOUNDS_ERROR = 'Could not extract bounds from string {string}.'

    def __init__(self):
        pass


Coordinate = Tuple[int, int]


def get_uploaded_image(uploader: FileUpload) -> PIL.Image.Image:
    if not uploader.value:
        raise ValueError(ErrorMessage.UPLOAD_ERROR)
    file_info = next(iter(uploader.value.values()))
    image = PIL.Image.open(io.BytesIO(file_info['content'])).convert('RGB')
    return image


def parse_bounds(bound_string: str) -> Tuple[Coordinate, Coordinate]:
    regex = r'\[([0-9]+),([0-9]+)\]\[([0-9]+),([0-9]+)\]'
    m = re.match(regex, bound_string)
    if m is None:
        raise ValueError(ErrorMessage.BOUNDS_ERROR.format(string=bound_string))
    top_left = (int(m.group(1)), int(m.group(2)))
    bottom_right = (int(m.group(3)), int(m.group(4)))
    return top_left, bottom_right


def draw_bounding_box(
        image: PIL.Image.Image,
        top_left: Coordinate,
        bottom_right: Coordinate,
) -> PIL.Image.Image:
    duplicate_image = image.copy()
    draw = PIL.ImageDraw.Draw(duplicate_image)
    draw.rectangle([top_left, bottom_right], outline="red", width=10)
    return duplicate_image


def crop_image(
        image: PIL.Image.Image,
        top_left: Coordinate,
        bottom_right: Coordinate,
) -> PIL.Image.Image:
    return image.crop([*top_left, *bottom_right])


def convert_image_to_bytes(image: PIL.Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def get_bottom_right(
        image: PIL.Image.Image,
        top_left: Coordinate,
) -> Coordinate:
    width, height = image.size
    bottom = top_left[1] + height
    right = top_left[0] + width
    return right, bottom
