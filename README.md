# Covid NZ QR Code Generator

Your QR code json file should has five fields:

| Field | Meaning |
| --- | --- |
| gin | This is the global identifier number. This is something that businesses have to apply for, so you probably don't have one. Just set it as anything (it does show in the app) |
| ver | Probably just a QR code version number. As far as I can tell, this doesn't matter |
| typ | The type of scan this is. As far as I know, "entry" is the only type but there may be more |
| opn | The place name. This is what shows up at the top. This would typically be a business's name |
| adr | This is the address. As usual, this can be anything. You can use `\n` characters to add new lines. |

The json is converted to base64 and the b64 string has `NZCOVIDTRACER:` appended to the start of it.
