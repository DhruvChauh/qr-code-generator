Usage examples:

  python qr_generator.py --text "https://example.com" --output example.png
  
  python qr_generator.py --file input.txt --output fromfile.png
  
  python qr_generator.py --text "BEGIN:VCARD\nFN:Dhruv Chauhan\nTEL:+911234567890\nEND:VCARD" --output contact.png
  
  python qr_generator.py --text "https://example.com" --output example.svg --format svg

Install dependencies:

  pip install qrcode[pil] pillow
  
qrcode[pil] brings qrcode and Pillow. For SVG output, qrcode already supports it.   

