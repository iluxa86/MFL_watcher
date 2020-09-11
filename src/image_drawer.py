from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


class ImageDrawer:
    _font = None
    _base_image = None
    _height = None
    _width = None
    _offset = 20

    def __init__(self, base_image=None, font=None, font_size=None):
        self._base_image = Image.open(base_image).convert('RGBA')
        self._height = self._base_image.height
        self._width = self._base_image.width

        if not font_size:
            font_size = round(self._height / 10)
        self._font = ImageFont.truetype(font, font_size)

    def put_teams_on_image(self, team1, team2, binary = False):
        image = self._base_image.copy()
        draw = ImageDraw.Draw(image)

        draw.multiline_text(
            xy=(self._offset, self._offset),
            text='\n'.join(self.__split_team_name(team1)),
            font=self._font,
            fill="black",
            align="left"
        )

        # Calculate pos for second text
        t2 = self.__split_team_name(team2)
        w2 = 0
        h2 = 0
        for t in t2:
            w, h = self._font.getsize(t)
            if w > w2:
                w2 = w
            h2 = h2 + h

        draw.multiline_text(
            xy=(self._width - self._offset - w2, self._height - self._offset - h2),
            text='\n'.join(t2),
            font=self._font,
            fill="black",
            align="right"
        )

        return self.__to_binary(image) if binary else image

    @staticmethod
    def __split_team_name(team_name):
        name_list = team_name.split()
        line1 = ""
        line2 = ""
        while len(name_list) > 0:
            if len(line1) <= len(line2):
                line1 = line1 + " " + name_list.pop(0)
            else:
                line2 = line2 + " " + name_list.pop()
        return [line1.strip(), line2.strip()]

    @staticmethod
    def __to_binary(image):
        bytes_io = BytesIO()
        bytes_io.seek(0)
        image.save(bytes_io, format="png")
        bytes_io.seek(0)
        return bytes_io


#id = ImageDrawer(base_image='../images/DIV05.png', font='../images/BAUHS93.ttf')
#im = id.put_teams_on_image( "LINKOR October Revolution", "The Louserville Redemption", binary=True)

#from telegrambot import TelegramBot
#bot = TelegramBot()
#bot.send_message("Тестовый трейд между какими-то лохами", im)