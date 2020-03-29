import argparse
import datetime
from pathlib import Path
import random
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



# TODO: pass these in
# band_name = "Vulnerable\nVMs"
# 'Von Neumann Bottleneck')
# band_name = "def no await"
band_name = "2 Pallas"

def download_all_images(search):
    print(f"Searching for: {search}")
    page = wikipedia.page(search)
    for image_url in page.images:
        Path(f"images/{search}").mkdir(exist_ok=True)
        image_name = f"{search}/{Path(image_url).parts[-1]}"
        print(image_name)
        urllib.request.urlretrieve(image_url, f"images/{image_name}")


def rainbow_affect(img):
    frequency = 3
    phase_shift = -90
    amplitude = 0.2
    bias = 0.7
    img.function('sinusoid', [frequency, phase_shift, amplitude, bias])

# Affects and Effects this
def add_band_name(img):
    with Drawing() as draw:
        # The font size needs to be proportional
        draw.font_size = int(img.width / 10)

        # We have to know when we are using light verus dark affects
        draw.fill_color = Color('white')
        # draw.fill_color = Color('rgba(3, 3, 3, 0.6)')
        draw.font = 'Inconsolata-Bold'
        draw.text(int(img.width / random.randint(2,4)), int(img.height /
            random.randint(2,4)), band_name)

        # draw.text(100, 100, band_name)
        draw(img)


def rainbow_img(img):
    rainbow_affect(img)

def sketch_img(img):
    img.kuwahara(radius=2, sigma=1.5)


def edit_image(image_path, edit_func):
    with Image(filename=image_path) as img:
        print(f"{image_path} Width: {img.width} Height: {img.height}")

        add_band_name(img)

        edit_func(img)

        image_folder, search, filename = image_path.parts
        save_filename = Path(__file__).parent.joinpath(
            f"images/{search}/album_art/tint-{filename}-{time.time()}"
        )
        img.save(filename=save_filename)


def tint_img(img):
    img.tint(color="blue", alpha="rgb(40%, 60%, 80%)")


def rainbow_img(img):
    rainbow_affect(img)


def sketch_img(img):
    img.kuwahara(radius=2, sigma=1.5)


def rotate_blur_img(img):
    img.rotational_blur(angle=4)


def pixel_spread_img(img):
    img.spread(radius=8.0)


def black_and_white_img(img):
    img.transform_colorspace('gray')
    img.edge(radius=1)


def sketch_img(img):
    img.transform_colorspace("gray")
    img.sketch(0.5, 0.0, 98.0)


def border_img(img):
    img.vignette(sigma=3, x=10, y=10)


EFFECTS = [rainbow_img, sketch_img, tint_img, rotate_blur_img, rotate_blur_img,
        pixel_spread_img, black_and_white_img, sketch_img, border_img]


def produce_samples(search):
    Path(__file__).parent.joinpath(f"images/{search}/album_art").mkdir(exist_ok=True)

    image_folder = Path(__file__).parent.joinpath(f"images/{search}")

    for image in image_folder.glob("*.jpg"):
        print(image)
        for effect in EFFECTS:
            edit_image(image, effect)
            # effect(image_folder.joinpath(image))

        
    # image_name = "{search}/Luftballong.jpg"
    # image_path = Path(__file__).parent.joinpath(f"images/{image_name}")
    # This should remove images of a certain size and filetyppe

    # I can use imagemagick to read width






# # What's the most efficent way to call
# # a bunch of different effects on the same image
# with Image(filename=image_filename) as img:
#     print(img.width, img.height)


#     add_band_name(img)
    # Should we start saving the affects in the title

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
        # poseidonbl: search term djengis khan
        # image_name = "Balloons/Jacques_Charles_Luftschiff.jpg"
        # image_name = "Balloons/Parada_Gay_em_Sampa.jpg"

        produce_samples(args.search)
