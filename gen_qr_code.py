import base64
import random

import qrcode

values = [
    ("gln", "global location number", "{:013d}".format(random.randrange(10 ** 13))),
    ("ver", "version", "c19:1"),
    ("typ", "action type", "entry"),
    ("opn", "place name", None),
    ("adr", "address. Use \\n to indicate new lines", None),
]
inputs = {}


def validate_input(
    message: str, default_value: str = None,
):
    # Validation of input
    while True:
        data = input(message)
        if data:
            return data
        elif default_value:
            return default_value

    return data


for field, help_text, default in values:
    inputs[field] = validate_input(
        "Enter the {}".format(help_text)
        + (". Default value is {}".format(default) if default else "")
        + ": ",
        default_value=default,
    )

with open("qrcode_blank") as f:
    # Read json string
    json_qr = f.read()
    
    # Format string with user inputs
    json_qr = json_qr.format(**inputs)

    # Encode into base64
    encoded_qr = base64.b64encode(json_qr.encode()).decode()

    # Add "NZCOVIDTRACER:" to start of string
    qr_string = "NZCOVIDTRACER:{}".format(encoded_qr)

    # Generate a version 15 (77x77) QR code containing qr_string
    qr = qrcode.QRCode(version=15, error_correction=qrcode.constants.ERROR_CORRECT_H)
    img = qr.add_data(qr_string)
    qr.make()

    # Make the QR code and save the image
    img = qr.make_image()
    filename = "qr_code"
    filename = validate_input("Enter a filename to save as. Default name is {}: ".format(filename), default_value=filename)
    img.save("{}.png".format(filename))
