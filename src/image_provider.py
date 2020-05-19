from google_images_search import GoogleImagesSearch
from io import BytesIO
import watcherconfig as cfg
from logger import logger
import random
from PIL import Image


class ImageProvider:
    __api_key = cfg.mflwatcher['imageprovider_api_key']
    __search_engine = cfg.mflwatcher['imageprovider_search_engine']

    def __init__(self):
        self.__log = logger(self.__class__)
        self.__log.log("STARTING IMAGE PROVIDER")

    def get_player_image(self, player_full_name):

        try:
            gis = GoogleImagesSearch(self.__api_key, self.__search_engine)
            _search_params = {
                'q': player_full_name,
                'hq': 'NFL',
                'searchType': 'image',
                #'imgType': 'face',
                #'imgSize': 'LARGE',
                'num': 6
            }

            gis.search(search_params=_search_params)
            my_bytes_io = BytesIO()

            image = random.choice(gis.results())
            my_bytes_io.seek(0)
            image.copy_to(my_bytes_io)
            my_bytes_io.seek(0)
            return my_bytes_io
        except:
            return None

#ip = ImageProvider()
#ip.get_player_image("Tua Tagovailoa")
#Image.open(ip.get_player_image("Tua Tagovailoa")).show()