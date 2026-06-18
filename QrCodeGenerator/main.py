import qrcode

url = input("Enter the URL: ").strip()
filepath = "qrcodesaver/qrcode.png"

qr = qrcode.QRCode()
qr.add_data(url)

img = qr.make_image()
img.save(filepath)

print("Qr Code Was Generated")