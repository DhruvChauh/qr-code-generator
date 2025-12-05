#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

def ensure_dependencies():
    try:
        import qrcode
        from PIL import Image
    except Exception as e:
        print("Missing dependency. Install with:")
        print("  pip install qrcode[pil]")
        sys.exit(1)

def generate_png(text: str, out_path: Path, box_size: int = 10, border: int = 4, error_correction='M'):
    import qrcode
    from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    from PIL import Image

    ec_map = {'L': ERROR_CORRECT_L, 'M': ERROR_CORRECT_M, 'Q': ERROR_CORRECT_Q, 'H': ERROR_CORRECT_H}
    ec = ec_map.get(error_correction.upper(), ERROR_CORRECT_M)

    qr = qrcode.QRCode(
        version=None, 
        error_correction=ec,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)
    print(f"Saved PNG QR code to: {out_path}")

def generate_svg(text: str, out_path: Path, box_size: int = 10, border: int = 4, error_correction='M'):
    import qrcode
    from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    from qrcode.image.svg import SvgImage
    ec_map = {'L': ERROR_CORRECT_L, 'M': ERROR_CORRECT_M, 'Q': ERROR_CORRECT_Q, 'H': ERROR_CORRECT_H}
    ec = ec_map.get(error_correction.upper(), ERROR_CORRECT_M)

    qr = qrcode.QRCode(
        version=None,
        error_correction=ec,
        box_size=box_size,
        border=border,
        image_factory=SvgImage
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image()
    with open(out_path, 'wb') as f:
        f.write(img.to_string())
    print(f"Saved SVG QR code to: {out_path}")

def parse_args():
    p = argparse.ArgumentParser(description="Small QR code generator (PNG or SVG).")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', '-t', help="Text to encode in the QR code (wrap vCard/URLs in quotes).")
    group.add_argument('--file', '-f', type=Path, help="Read text to encode from a file.")
    p.add_argument('--output', '-o', type=Path, default=Path('qrcode.png'), help="Output file path (png or svg).")
    p.add_argument('--format', choices=['png', 'svg'], default=None, help="Force output format (png or svg).")
    p.add_argument('--box-size', type=int, default=10, help="Size of each QR box (pixels for PNG).")
    p.add_argument('--border', type=int, default=4, help="Border size (boxes).")
    p.add_argument('--error', choices=['L','M','Q','H'], default='M', help="Error correction level: L,M,Q,H.")
    return p.parse_args()

def main():
    ensure_dependencies()
    args = parse_args()

    if args.file:
        if not args.file.exists():
            print("Input file not found:", args.file)
            sys.exit(1)
        text = args.file.read_text(encoding='utf-8')
    else:
        text = args.text

    out = args.output
    fmt = (args.format or out.suffix.lstrip('.')).lower()
    if fmt not in ('png','svg'):
        fmt = 'png'
        if out.suffix == '':
            out = out.with_suffix('.png')

    out.parent.mkdir(parents=True, exist_ok=True)

    if fmt == 'png':
        generate_png(text, out, box_size=args.box_size, border=args.border, error_correction=args.error)
    else:
        generate_svg(text, out, box_size=args.box_size, border=args.border, error_correction=args.error)

if __name__ == '__main__':
    main()
