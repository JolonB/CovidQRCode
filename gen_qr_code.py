import base64
import random

import qrcode
from PIL import Image

values = [
    ("gln", "global location number", "{:013d}".format(random.randrange(10 ** 13))),
    ("ver", "version", "c19:1"),
    ("typ", "action type", "entry"),
    ("opn", "place name", None),
    ("adr", "address. Use \\n to indicate new lines", None),
]
inputs = {}


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
        poster = Image.open('assets/poster_blank.jpg')
        img = draw_on_image(poster, img, (284,295), (1163,1174))

    # Save the image
    filename = "qr_code"
    filename = validate_input("Enter a filename to save as. Default name is {}: ".format(filename), default_value=filename)
    img.save("{}.png".format(filename))
