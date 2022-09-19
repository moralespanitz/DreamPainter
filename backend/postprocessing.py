"""
Post processing image
---------------------
- Add UTEC Mark 
- Add hashtag
"""
import PIL
from PIL import Image

class PostProcessing:
    def __init__(self) -> None:
        self.image : Image

    def _add_mark_water(self) -> Image:
        # TODO: Add mark water
        self.mark_water = self.image
        return self.mark_water

    def _add_hashtag(self) -> Image:
        # TODO: Add hashtag
        self.hashtag = self.image
        return self.hashtag

    def get_image(self, image : Image) -> Image:
        try:
            # Set image
            self.image = image
            self.hash = self._add_hashtag(self.image)
            self.mark = self._add_hashtag(self.hash)
            return self.mark
        except:
            assert "Error while preprocessing image"
