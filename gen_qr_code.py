import base64
import random

import qrcode
from PIL import Image, ImageDraw, ImageFont

values = [
    ("gln", "global location number", "{:013d}".format(random.randrange(10 ** 13))),
    ("ver", "version", "c19:1"),
    ("typ", "action type", "entry"),
    ("opn", "place name", None),
    ("adr", "address. Use \\n to indicate new lines", None),
]
inputs = {}

TITLE_SIZE = 30
SUBTITLE_SIZE = 25
TITLE_FILE = "font/title.ttf"
SUBTITLE_FILE = "font/subtitle.ttf"


def validate_input(
    message: str, default_value: str = None, class_:type=None, valid_values:list=None,
):
    # Validation of input
    while True:
        response = None
        try:
            data = input(message)
            if data:
                response = class_(data) if class_ else data
            elif default_value:
                response = default_value
        except ValueError:
            print("Please enter a value of type {}.".format(class_))
            continue
        
        # Return response if there is no list of valid values, or the response is in it if there is one
        if not valid_values or response in valid_values:
            return response
        else:
            print("Response is not valid. Must be one of {}".format(valid_values))
            continue


def draw_on_image(background:Image, foreground:Image, topleft:tuple, bottomright:tuple):
    x_tl, y_tl = topleft
    x_br, y_br = bottomright

    width, height = (x_br - x_tl), (y_br - y_tl)

    foreground = foreground.resize((width, height)) 
    # Create a copy of the background before pasting so the original doesn't change
    background = background.copy()
    background.paste(foreground, topleft)

    return background

def remove_n(string:str):
    return string.replace('\\n', ', ')

def create_poster(foreground:Image, title:str, subtitle:str):
    # Get poster
    poster = Image.open('assets/poster_blank.jpg')
    width, height = poster.size

    # Draw QR code on it
    topleft = (int(0.2*width), int(0.144*height))
    bottomright = (int(166/207*width), int(587/1024*height))
    img = draw_on_image(poster, foreground, topleft, bottomright) # (284,295), (1163,1174) for 1449x2048 poster

    # Add text
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype(TITLE_FILE, TITLE_SIZE)
    subtitle_font = ImageFont.truetype(SUBTITLE_FILE, SUBTITLE_SIZE)
    title_x0, title_y0, title_x1, title_y1 = title_font.getbbox(title)
    subtitle_x0, subtitle_y0, subtitle_x1, subtitle_y1 = subtitle_font.getbbox(subtitle)

    title_w = title_x1 - title_x0
    subtitle_w = subtitle_x1 - subtitle_x0
    draw.text(((width-title_w)/2, 1215-title_y0), title, font=title_font, fill="black")
    draw.text(((width-subtitle_w)/2, 1260 - subtitle_y0), subtitle, font=subtitle_font, fill="black") # TODO allow this to be changed based on poster size

    return img

for field, help_text, default in values:
    inputs[field] = validate_input(
        "Enter the {}".format(help_text)
        + (". Default value is \"{}\"".format(default) if default else "")
        + ": ",
        default_value=default,
    )

with open("assets/qrcode_blank") as f:
    # Read json string
    json_qr = f.read()
    
    # Format string with user inputs
    json_qr = json_qr.format(**inputs)

    # Encode into base64
    encoded_qr = base64.b64encode(json_qr.encode()).decode()

    # Add "NZCOVIDTRACER:" to start of string
    qr_string = "NZCOVIDTRACER:{}".format(encoded_qr)

    # Generate a version 15 (77x77) QR code containing qr_string
    qr = qrcode.QRCode(version=15, error_correction=qrcode.constants.ERROR_CORRECT_L)
    img = qr.add_data(qr_string)
    qr.make()

    # Make the QR code
    img = qr.make_image()

    # Check if user wants a poster
    poster_yn = validate_input("Would you like this in poster form? If \"n\", only the QR code will be saved. [Y/n]: ", default_value='y', class_=str.lower, valid_values=['y','n'])
    if poster_yn == 'y':
        title = remove_n(inputs['opn'])
        title = validate_input("Enter a title. Default is {}. \"\\n\" will be replaced by \", \": ".format(title), default_value=title)
        subtitle = remove_n(inputs['adr'])
        subtitle = validate_input("Enter a title. Default is {}. \"\\n\" will be replaced by \", \": ".format(subtitle), default_value=subtitle)
        img = create_poster(img, title, subtitle)        

    # Save the image
    filename = "qr_code"
    filename = validate_input("Enter a filename to save as. Default name is {}: ".format(filename), default_value=filename)
    img.save("{}.png".format(filename))


# title_font = ImageFont.truetype('font/title.ttf', 20)
# subtitle_font = ImageFont.truetype('font/subtitle.ttf', 20)