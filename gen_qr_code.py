import base64
import qrcode

with open("qrcode.json") as f:
    json_qr = f.read()

    encoded_qr = base64.b64encode(json_qr.encode()).decode()

    qr_string = "NZCOVIDTRACER:" + encoded_qr

    img = qrcode.make(qr_string)

    print(img)

    img.save("qr_code.png")

    print(qr_string)