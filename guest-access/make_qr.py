#!/usr/bin/env python3
"""
Generate the QR code for the Guest Access Portal sign.

Usage:
    python make_qr.py                       # default URL, all sizes
    python make_qr.py https://example.com/x  # custom URL

Produces wifi-qr-<size>.png in this folder, ready to print.
Requires: pip install qrcode[pil]
"""

import sys
import os

DEFAULT_URL = "https://guest.church-registration-grace.web.app"

# Printed on an A4 sign. 1024 is plenty for a laser printer.
SIZES = [512, 1024]


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    url = url.rstrip("/")

    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_M
    except ImportError:
        sys.exit(
            "Missing dependency. Run:\n"
            "    pip install qrcode[pil]\n"
            "then re-run this script."
        )

    here = os.path.dirname(os.path.abspath(__file__))
    made = []

    # Resolve the module grid first so we can pick a box_size that lands on
    # the requested pixel width instead of guessing.
    probe = qrcode.QRCode(error_correction=ERROR_CORRECT_M, border=2)
    probe.add_data(url)
    probe.make(fit=True)
    total_modules = len(probe.get_matrix()) + 2 * probe.border

    for size in SIZES:
        # Keep an integer module size: QR codes stay crisp only when every
        # module is a whole number of pixels.
        box_size = max(1, round(size / total_modules))
        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_M,  # survives a bit of wear/smudge
            box_size=box_size,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#2c3e50", back_color="white").convert("RGB")

        path = os.path.join(here, f"wifi-qr-{size}.png")
        img.save(path, dpi=(300, 300))
        made.append((path, img.size, box_size))

    print(f"QR target URL: {url}")
    print(f"URL length: {len(url)} chars")
    print()
    for path, dim, box in made:
        print(f"  wrote {os.path.basename(path)}  ({dim[0]}x{dim[1]} px, module={box}px)")

    print(
        "\nPrint tips:\n"
        "  - Use wifi-qr-1024.png for A4/poster printing.\n"
        "  - Keep the white border (2 modules) - scanners need it.\n"
        "  - Print matte if possible; gloss causes screen glare.\n"
        "  - Do NOT print or hand out until the site is deployed, or the\n"
        "    scan will go nowhere.\n"
        "  - Test the printed code with 2-3 different phones before laminating."
    )


if __name__ == "__main__":
    main()