import random
import urllib.request

import wikipedia

search = "Forest"
page = wikipedia.page(search)
image_url = random.sample(page.images, 1)[0]
urllib.request.urlretrieve(image_url, "images/image_url.jpg")
