from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
import os
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_frontend():
    return send_file('front.html')

# --------------------
# Style functions
# --------------------

def convert_ghibli(img):
    img = img.convert('RGB')
    img = ImageEnhance.Color(img).enhance(1.3)
    overlay = Image.new('RGB', img.size, (255, 160, 60))
    img = Image.blend(img, overlay, 0.25)
    return img.filter(ImageFilter.GaussianBlur(radius=1.2))

def convert_doodles(img):
    img = img.convert('L')
    edges = img.filter(ImageFilter.FIND_EDGES)
    return ImageOps.invert(edges).convert('RGB')

def convert_watercolor(img):
    img = img.convert('RGB')
    img = ImageEnhance.Color(img).enhance(1.8)
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    pixels = overlay.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if random.random() < 0.03:
                pixels[i,j] = (200, 200, 180, 40)
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def convert_popart(img):
    img = img.convert('RGB')
    img = ImageOps.posterize(img, bits=3)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    return ImageEnhance.Brightness(img).enhance(1.2)

def convert_noir(img):
    img = img.convert('L')
    return img.point(lambda p: 255 if p > 128 else 0).convert('RGB')

def convert_sepia(img):
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    for py in range(height):
        for px in range(width):
            r, g, b = pixels[px, py]
            tr = int(0.393*r + 0.769*g + 0.189*b)
            tg = int(0.349*r + 0.686*g + 0.168*b)
            tb = int(0.272*r + 0.534*g + 0.131*b)
            pixels[px, py] = (min(tr,255), min(tg,255), min(tb,255))
    return img

def convert_sketch(img):
    img = img.convert('L')
    inverted = ImageOps.invert(img)
    blurred = inverted.filter(ImageFilter.GaussianBlur(10))
    width, height = img.size
    result = Image.new('L', (width, height))
    for y in range(height):
        for x in range(width):
            val = img.getpixel((x, y)) * 255 / (256 - blurred.getpixel((x, y)) + 1)
            result.putpixel((x, y), int(min(val, 255)))
    return result.convert('RGB')

def convert_emboss(img):
    return img.convert('RGB').filter(ImageFilter.EMBOSS)

def convert_posterize(img):
    return ImageOps.posterize(img.convert('RGB'), bits=4)

def convert_pixelate(img):
    small = img.resize((img.width//16, img.height//16), resample=Image.BILINEAR)
    return small.resize(img.size, Image.NEAREST)

def convert_solarize(img):
    return ImageOps.solarize(img.convert('RGB'), threshold=128)

def convert_vintage(img):
    img = img.convert('RGB')
    img = ImageOps.colorize(ImageOps.grayscale(img), black="#704214", white="#c0a080")
    return ImageEnhance.Brightness(img).enhance(1.1)

def convert_cartoon(img):
    img = img.convert('RGB')
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return ImageEnhance.Contrast(img).enhance(1.5)

def convert_neon_glow(img):
    img = img.convert('RGB')
    img = ImageEnhance.Color(img).enhance(2.5)
    return img.filter(ImageFilter.GaussianBlur(radius=2))

def convert_blur(img):
    return img.convert('RGB').filter(ImageFilter.GaussianBlur(radius=3))

# --------------------
# Main conversion route
# --------------------

@app.route('/api/convert', methods=['POST'])
def api_convert():
    if 'image' not in request.files or 'style' not in request.form:
        return jsonify({'error': 'Image file and style parameter required'}), 400

    image_file = request.files['image']
    style = request.form['style'].lower()

    try:
        img = Image.open(image_file.stream)
    except Exception as e:
        return jsonify({'error': f'Invalid image: {str(e)}'}), 400

    style_functions = {
        'ghibli': convert_ghibli,
        'doodles': convert_doodles,
        'watercolor': convert_watercolor,
        'popart': convert_popart,
        'noir': convert_noir,
        'sepia': convert_sepia,
        'sketch': convert_sketch,
        'emboss': convert_emboss,
        'posterize': convert_posterize,
        'pixelate': convert_pixelate,
        'solarize': convert_solarize,
        'vintage': convert_vintage,
        'cartoon': convert_cartoon,
        'neonglow': convert_neon_glow,
        'blur': convert_blur
    }

    if style not in style_functions:
        return jsonify({'error': 'Invalid style selected'}), 400

    result_img = style_functions[style](img)

    img_io = io.BytesIO()
    result_img.save(img_io, 'PNG', quality=90)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
