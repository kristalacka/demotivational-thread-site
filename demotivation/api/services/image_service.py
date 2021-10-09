from api.models import Post, Comment
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class ImageSerivce():
    def __init__(self):
        self.font_path = f'{settings.MEDIA_ROOT}/fonts/NewBaskervilleITCbyBT-Roman.otf'
        self.default_width_multiplier = 1.1  # generated image width
        self.default_height_multiplier = 1.25  # generated image height
        self.border_multiplier = 1.02  # how much bigger the border will be than the image
        self.primary_font_scale = 0.08  # font scale in relation to image height
        self.bottom_font_scale = 0.04  # bottom text font scale in relation to image height

    def generate_post_image(self, post: Post):
        image = self._generate_image(post.image_file, post.primary_text,
                                     post.bottom_text)
        return self._convert_to_django_img(image)

    def generate_comment_image(self, comment: Comment):
        if comment.parent is None:
            image_file = f"{settings.MEDIA_ROOT}/posts/{comment.post.id}/generated.png"
        else:
            image_file = f"{settings.MEDIA_ROOT}/posts/{comment.post.id}/comment_{comment.parent.id}.png"
        image = self._generate_image(image_file, comment.primary_text,
                                     comment.bottom_text)
        return self._convert_to_django_img(image)

    def _convert_to_django_img(self, image):
        buffer = BytesIO()
        image.save(fp=buffer, format='PNG')
        pillow_image = ContentFile(buffer.getvalue())
        return InMemoryUploadedFile(
            pillow_image,  # file
            None,  # field_name
            'image.png',  # file name
            'image/jpeg',  # content_type
            pillow_image.tell,  # size
            None)  # content_type_extra)

    def _get_image_width_multiplier(self, bottom_text: int,
                                    original_width: int):
        """
        Get image width multiplier so that bottom text would fit
        """
        return max(
            len(bottom_text) / (original_width / 10),
            self.default_width_multiplier)

    def _generate_image(self, previous_image: str, primary_text: str,
                        bottom_text: str):
        """
        Lord have mercy
        """
        pil_image = Image.open(previous_image)
        orig_size = pil_image.size

        # create black base
        new_width_multiplier = self._get_image_width_multiplier(
            bottom_text, orig_size[0])
        final_img_size = (int(new_width_multiplier * orig_size[0]),
                          int(self.default_height_multiplier * orig_size[1]))
        final_img = Image.new("RGB", final_img_size)

        # create white border
        border_size = tuple(
            [int(x * self.border_multiplier) for x in orig_size])
        border_x = int((final_img_size[0] - border_size[0]) / 2)
        y_coord = (int(self.default_width_multiplier * orig_size[0]) -
                   border_size[0]) // 2  # border starting y coordinate
        border_coords = [(border_x, y_coord),
                         (border_x + border_size[0], y_coord + border_size[1])]
        final_img_draw = ImageDraw.Draw(final_img)
        final_img_draw.rectangle(border_coords, fill="#000", outline="#fff")

        # insert original image
        center_x = (final_img_size[0] - orig_size[0]) // 2
        y_coord = (int(self.default_width_multiplier * orig_size[0]) -
                   orig_size[0]) // 2  # original image starting y coordinate
        final_img.paste(pil_image, (center_x, y_coord))

        font_size = int(self.primary_font_scale * orig_size[1])
        font = ImageFont.truetype(self.font_path, font_size)

        # insert primary text
        text_size = final_img_draw.textsize(primary_text.upper(), font=font)
        final_img_draw.text(
            ((final_img_size[0] - text_size[0]) / 2, border_size[1] + y_coord),
            primary_text.upper(), (255, 255, 255),
            font=font)

        # insert bottom text
        bottom_font_size = int(self.bottom_font_scale * orig_size[1])
        bottom_font = ImageFont.truetype(self.font_path, bottom_font_size)
        subtext_size = final_img_draw.textsize(bottom_text, font=bottom_font)
        final_img_draw.text(
            ((final_img_size[0] - subtext_size[0]) / 2,
             border_size[1] + y_coord + text_size[1] + subtext_size[1]),
            bottom_text, (255, 255, 255),
            font=bottom_font)

        return final_img
