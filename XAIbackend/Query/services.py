import os
from typing import Any, Tuple


def parse_query_input(query_input: Any) -> Tuple[Any, str]:
    input_type = "tabular"
    input_data = query_input

    if isinstance(input_data, dict):
        for key, value in input_data.items():
            if isinstance(value, str) and _is_image_path(value):
                image = _load_image(value)
                if image is not None:
                    input_data[key] = image
                    input_type = "image"

    return input_data, input_type


def _is_image_path(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    lowered = path.lower()
    return lowered.endswith(".png") or lowered.endswith(".jpg") or lowered.endswith(".jpeg")


def _load_image(path: str):
    import cv2

    return cv2.imread(path)
