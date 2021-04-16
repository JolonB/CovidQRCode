# Covid NZ QR Code Generator

Your QR code has five fields:

| Field | Meaning |
| --- | --- |
| gin | This is the global identifier number. This is something that businesses have to apply for, so you probably don't have one. Just set it as anything (it does show in the app) |
| ver | Probably just a QR code version number. As far as I can tell, this doesn't matter |
| typ | The type of scan this is. As far as I know, "entry" is the only type but there may be more |
| opn | The place name. This is what shows up at the top. This would typically be a business's name |
| adr | This is the address. As usual, this can be anything. You can use `\n` characters to add new lines. |

To run the code, first install the requirements with `pip install -r requirements.txt`.
Next run the code with `python gen_qr_code.py`.  
The program will ask you for you inputs into the fields.
Some of these have default values, so you can simply press enter to autofill it.
