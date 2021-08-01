import glob
from datetime import datetime
from random import choice, seed, random
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps

seed(datetime.now())


def font_size_from_shape_text(width: int, height: int, text: str) -> int:
    return (height * width) // (500 * len(text))


def get_dante_image():
    files = list(glob.glob("imgs/*.jpg"))
    return choice(files)


def get_font():
    files = list(glob.glob("fonts/*.ttf"))
    return choice(files)


def get_random_text_angle():
    return random() * 100


def create_dale_dante():
    text = "Dale Dante!"
    dante_image_name = get_dante_image()
    im = Image.open(dante_image_name)
    font_size = font_size_from_shape_text(im.width, im.height, text)
    font = ImageFont.truetype(get_font(), font_size)
    txt = Image.new('L', (500, 500))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), text, font=font, fill=255)
    angle = get_random_text_angle()
    w = txt.rotate(angle, expand=1)
    im.paste(ImageOps.colorize(w, (0, 0, 0), (255, 0, 255)), (242, 60), w)
    bio = BytesIO()
    bio.name = 'image.jpeg'
    im.save(bio, 'JPEG')
    bio.seek(0)
    return bio


