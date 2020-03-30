import argparse
import datetime
from faker import Faker
import functools
from pathlib import Path
import random
from random import randint
import time
import urllib.request

from wand.image import Image
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
import wikipedia

# Need to be smarter about taking in a URL name

# - We take in a band name from viewers
# - We take in words to describe the band
# - We pull photos from wikipedia
# - We generate a bunch of random photos based on the input
# - We then choose one

# # Long Term Goals

# - Blue Note record generator
# - Other Genre Album generator

fake = Faker()

DICT_WORDS = Path("/usr/share/dict/cracklib-small").read_text().split()

# The singlewords
# The singleword project
# 1 to 4 words
def band_name_generator():
    band_name_length = randint(1, 2)

    if band_name_length == 2:
        # The most pythonic 50% this or that
        return " ".join(random.sample(DICT_WORDS, band_name_length))
    else:

        if randint(0,1) == 0:
            return " ".join(random.sample(DICT_WORDS, band_name_length))
        else:
            return "The {random.sample(DICT_WORDS, 1)[0].upper()}'s"



def download_all_images(search):
    print(f"Searching for: {search}")
    page = wikipedia.page(search)
    for image_url in page.images:
        Path(f"images/{search}").mkdir(exist_ok=True)
        image_name = f"{search}/{Path(image_url).parts[-1]}"
        print(image_name)
        urllib.request.urlretrieve(image_url, f"images/{image_name}")


# Affects and Effects this
def add_band_name(band_name, img):
    with Drawing() as draw:
        # The font size needs to be proportional
        draw.font_size = int(img.width / random.randint(9, 20))

        # We have to know when we are using light verus dark affects
        color = fake.safe_color_name()

        draw.fill_color = Color(color)

        # draw.fill_color = Color('white')
        # draw.fill_color = Color('rgba(3, 3, 3, 0.6)')
        

        fonts = [
            'Inconsolata-Bold',
            "Cantarell-Regular"
        ]

        font = random.sample(fonts, 1)[0]
        draw.font = font


        draw.text(int(img.width / random.randint(4,8)), int(img.height /
            random.randint(3,6)), band_name)

        # draw.text(100, 100, band_name)
        draw(img)


def rainbow_img(img):
    frequency = random.randint(1,5)
    phase_shift = -90
    amplitude = 0.2
    bias = 0.7
    print(f"{frequency=}")
    print(f"{phase_shift=}")
    print(f"{amplitude=}")
    print(f"{bias=}")

    img.function('sinusoid', [frequency, phase_shift, amplitude, bias])



def tint_img(img):
    color = fake.safe_color_name()
    print(f"Tint: {color=}")
    img.tint(color=color, alpha="rgb(40%, 60%, 80%)")


def sketch_img(img):
    radius = random.randint(1,3)
    print(f"Sketch: {radius=}")
    img.kuwahara(radius=radius, sigma=1.5)


def rotate_blur_img(img):
    angle = random.randint(2,6)
    print(f"Rotate Blur: {angle=}")
    img.rotational_blur(angle=angle)


def pixel_spread_img(img):
    radius = random.randint(6,10)
    print(f"Pixel Spread: {radius=}")

    # Does this need to be a float??
    img.spread(radius=radius)


def black_and_white_img(img):
    img.transform_colorspace('gray')
    img.edge(radius=1)


def sketch_img(img):
    img.transform_colorspace("gray")
    img.sketch(0.5, 0.0, 98.0)


def border_img(img):
    sigma = random.randint(1,5)
    print(f"Border Image: {sigma=}")
    img.vignette(sigma=sigma, x=10, y=10)


EFFECTS = [rainbow_img, sketch_img, tint_img, rotate_blur_img, rotate_blur_img,
        pixel_spread_img, black_and_white_img, sketch_img, border_img]


def produce_samples(search):
    Path(__file__).parent.joinpath(f"images/{search}/album_art").mkdir(exist_ok=True)
    image_folder = Path(__file__).parent.joinpath(f"images/{search}")
    for image in image_folder.glob("*.jpg"):
        print(image)
        for effect in EFFECTS:
            band_name = band_name_generator()
            edit_image(image, effect, band_name)

    for image in image_folder.glob("*.jpg"):
        print(image)
        super_effects = random.sample(EFFECTS, random.randint(2, len(EFFECTS)))
        for effect in super_effects:
            effect(image)

        image_folder, search, filename = image.parts
        save_filename = Path(__file__).parent.joinpath(
            f"images/{search}/album_art/tint-{filename}-{time.time()}"
        )
        img.save(filename=save_filename)




def edit_image(image_path, edit_func, band_name):
    with Image(filename=image_path) as img:
        print(f"{image_path} Width: {img.width} Height: {img.height}")
        
        band_name_func = functools.partial(add_band_name, band_name)

        image_funcs = [edit_func, band_name_func]
        # random.shuffle(image_funcs)

        for image_func in image_funcs:
            image_func(img)

        image_folder, search, filename = image_path.parts
        save_filename = Path(__file__).parent.joinpath(
            f"images/{search}/album_art/tint-{filename}-{time.time()}"
        )
        img.save(filename=save_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sandberg Options")

    parser.add_argument(
        "--search", "-s", dest="search", help="What images to search and download from Wikipedia"
    )
    parser.add_argument(
      "--download", "-d", action="store_true", default=False, dest="download",
      help="Wether to download the images from the Wikipedia search"
  )
    args = parser.parse_args()

    if args.download:
        download_all_images(args.search)
    else:
        produce_samples(args.search)
