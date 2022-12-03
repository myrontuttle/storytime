from typing import Dict, Optional

import random

import requests

from storytime.gpt3 import generate_image
from storytime.scene import Scene


class ImageSet:
    """Set of images to accompany scenes in a story."""

    art_mediums = [
        "charcoal",
        "tempera",
        "oil painting",
        "stained glass",
        "watercolor",
        "acrylic",
        "chalk",
        "pen and ink",
        "pencil",
        "soft pastel",
        "colored pencil",
        "crayon",
        "oil pastel",
        "collage",
        "airbrush",
        "photographic",
        "digital art",
        "pixel art",
        "vector art",
        "photobashing",
        "photo painting",
        "digital collage",
        "3d art",
    ]

    art_styles = [
        "primitivist",
        "folk art",
        "renaissance",
        "ukiyo-e",
        "figurative",
        "surreal",
        "expressionist",
        "impressionist",
        "pointillist",
        "post-impressionist",
        "dadaist",
        "art novueau",
        "pop art",
        "cubist",
        "fauvist",
        "modern art",
        "geometric",
        "minimalist",
        "realistic",
        "semi-realistic",
        "symbolic",
        "postmodern art",
        "futuristic",
        "street art",
        "concept art",
        "cartoon",
        "anime",
        "aesthetic",
        "fantasy",
        "caricature",
        "doodles",
        "disney",
        "pixar",
    ]

    def __init__(
        self,
        medium: Optional[str] = None,
        style: Optional[str] = None,
    ) -> None:
        """Initialize ImageSet class."""
        if medium is None:
            self.medium = random.choice(self.art_mediums)
        else:
            self.medium = medium
        if style is None:
            self.style = random.choice(self.art_styles)
        else:
            self.style = style
        self.images: Dict[str, str] = {}

    def add_scene_image(self, label: str, scene: "Scene") -> None:
        """Add a generated image to the ImageSet based on a scene."""
        prompt = (
            f"A {self.medium} scene with a {self.style} style. A "
            f"{scene.location.area} {scene.location.locale} at "
            f"{scene.time_period.time_of_day} in "
            f"{scene.time_period.season}. {scene.scene_visual}"
        )
        self.images[label] = generate_image(prompt)

    def save_images(self, save_dir: str) -> None:
        """Save images to disk."""
        for label, image_url in self.images.items():
            if image_url is not None and len(image_url) > 0:
                img_data = requests.get(image_url).content
                with open(f"{save_dir}{label}.png", "wb") as handler:
                    handler.write(img_data)
