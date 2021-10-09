from api.models import Post, Comment
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings


class ImageSerivce():
    def __init__(self):
        self.font_path = f'{settings.MEDIA_ROOT}/fonts/NewBaskervilleITCbyBT-Roman.otf'

    def generate_post_image(self, post: Post):
        image = self._generate_image(post.image_file, post.primary_text,
                                     post.bottom_text)
        path = f"{settings.MEDIA_ROOT}/posts/{post.id}/generated.png"
        image.save(path)

    def generate_comment_image(self, comment: Comment):
        if comment.parent is None:
            image_file = f"{settings.MEDIA_ROOT}/posts/{comment.post.id}/generated.png"
        else:
            image_file = f"{settings.MEDIA_ROOT}/posts/{comment.post.id}/comment_{comment.parent.id}.png"
        image = self._generate_image(image_file, comment.primary_text,
                                     comment.bottom_text)
        path = f"{settings.MEDIA_ROOT}/posts/{comment.post.id}/comment_{comment.id}.png"
        image.save(path)

    def _get_image_width(self, bottom_text: int, original_width: int):
        return max(len(bottom_text) / (original_width / 10), 1.1)

    def _generate_image(self, previous_image: str, primary_text: str,
                        bottom_text: str):
        """
        Lord have mercy
        """
        pil_image = Image.open(previous_image)
        orig_size = pil_image.size

        new_width = self._get_image_width(bottom_text, orig_size[0])
        final_img_size = (int(new_width * orig_size[0]),
                          int(1.3 * orig_size[1]))
        final_img = Image.new("RGB", final_img_size)

        border_size = 1.02
        border_size = tuple([int(x * border_size) for x in orig_size])
        border_x = int((final_img_size[0] - border_size[0]) / 2)
        y_coord = (int(1.1 * orig_size[0]) - border_size[0]) // 2
        border_coords = [(border_x, y_coord),
                         (border_x + border_size[0], y_coord + border_size[1])]
        final_img_draw = ImageDraw.Draw(final_img)
        final_img_draw.rectangle(border_coords, fill="#000", outline="#fff")

        center_x = (final_img_size[0] - orig_size[0]) // 2
        y_coord = (int(1.1 * orig_size[0]) - orig_size[0]) // 2
        final_img.paste(pil_image, (center_x, y_coord))

        font_scale = 0.08
        font_size = int(font_scale * orig_size[1])
        font = ImageFont.truetype(self.font_path, font_size)

        text_size = final_img_draw.textsize(primary_text.upper(), font=font)
        final_img_draw.text(
            ((final_img_size[0] - text_size[0]) / 2, border_size[1] + y_coord),
            primary_text.upper(), (255, 255, 255),
            font=font)

        bottom_font_scale = font_scale / 2
        bottom_font_size = int(bottom_font_scale * orig_size[1])
        bottom_font = ImageFont.truetype(self.font_path, bottom_font_size)
        subtext_size = final_img_draw.textsize(bottom_text, font=bottom_font)
        final_img_draw.text(
            ((final_img_size[0] - subtext_size[0]) / 2,
             border_size[1] + y_coord + text_size[1] + subtext_size[1]),
            bottom_text, (255, 255, 255),
            font=bottom_font)

        return final_img
