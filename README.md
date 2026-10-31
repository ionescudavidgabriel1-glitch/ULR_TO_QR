# URL to QR Code

A small Flask web app that turns a URL into a QR code PNG. The QR code is built from scratch in Python: the data encoding, Reed-Solomon error correction, matrix layout and PNG rendering are all implemented in [URL_TO_QR.py](URL_TO_QR.py), without a QR library.

## Features

- Web interface for entering a URL and downloading the QR code as a PNG
- Choice of error correction level: L (7%), M (15%), Q (25%), H (30%)
- Automatically picks the smallest QR version (1 to 7) that fits the URL
- Reed-Solomon error correction over GF(256), with block interleaving
- JSON API endpoint that returns the QR code image

## How it works

[URL_TO_QR.py](URL_TO_QR.py) runs the QR encoding pipeline in nine steps:

1. **Validation and version selection**: the URL is encoded as UTF-8 and the smallest version whose capacity fits it is chosen for the requested error correction level.
2. **Data encoding**: the data is written in byte mode (`0100`) with an 8-bit length field, followed by a terminator and padding with the alternating bytes `0xEC` and `0x11`.
3. **Error correction**: the data codewords are split into blocks and each block gets Reed-Solomon error correction codewords. The blocks are then interleaved.
4. **Matrix setup**: finder, alignment and timing patterns, the dark module, and the format and version areas are placed in the matrix.
5. **Data placement**: the bitstream is written in the standard zig-zag order.
6. **Masking and format information**: a mask is applied and the 15-bit format string is written.
7. **Rendering**: the matrix is drawn with a 4-module quiet zone and 10 px per module, and returned as a PNG in memory.

## Limits

| Error correction | Maximum URL length (bytes) |
|------------------|----------------------------|
| L                | 154                        |
| M                | 122                        |
| Q                | 86                         |
| H                | 64                         |

Lengths are counted in UTF-8 bytes. Longer URLs are rejected.

## Requirements

- Python 3
- [Flask](https://pypi.org/project/Flask/)
- [Pillow](https://pypi.org/project/Pillow/)

Install them with:

```bash
pip install flask pillow
```

## Running the web app

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser, enter a URL, choose an error correction level, and click **Generate QR Code**. Use **Download Image** to save the result.

The server runs in Flask debug mode on port 5000. Turn debug mode off before deploying it anywhere public.

## API

### `POST /generate`

Request body (JSON):

```json
{
  "url": "https://example.com",
  "ec_level": "M"
}
```

- `url` (required): the text to encode
- `ec_level` (optional): `L`, `M`, `Q` or `H`. Defaults to `L`.

Responses:

- `200 OK` with `image/png` body: the QR code
- `400 Bad Request` with `{"error": "URL is required"}` if `url` is empty
- `500 Internal Server Error` with `{"error": "..."}` if generation fails

Example with `curl`:

```bash
curl -X POST http://127.0.0.1:5000/generate \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com", "ec_level": "H"}' \
     --output qr.png
```

## Using the generator from Python

`generate_qr_code` returns an in-memory PNG buffer:

```python
from URL_TO_QR import generate_qr_code

buffer = generate_qr_code("https://example.com", ec_level="Q")

with open("qr.png", "wb") as f:
    f.write(buffer.read())
```

The function prints its progress (selected version, block count and so on) to the console.

## Project structure

```
QR_code_project/
├── app.py              # Flask app: serves the page and the /generate endpoint
├── URL_TO_QR.py        # QR code generator (encoding, Reed-Solomon, rendering)
├── templates/
│   └── index.html      # Front-end form (Tailwind CSS via CDN)
├── generated_qr.png    # Sample output
└── .gitignore
```

## Known limitations

- Only QR versions 1 to 7 are supported, and only byte mode is used.
- The mask pattern is fixed to mask 0 instead of evaluating all eight masks and picking the best one. Most scanners read these codes, but some may have trouble with certain inputs.
- The front end loads Tailwind CSS from a CDN, so it needs an internet connection.
- If a URL is too long for version 7, the generator calls `sys.exit` instead of raising an ordinary exception, so the API does not return the JSON error message it is designed to return.
