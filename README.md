# Art Style Converter

A web application that allows users to convert their images into various art styles using Python and Flask.

## Features

- 15 different art styles including:
  - Ghibli
  - Doodles
  - Watercolor
  - Pop Art
  - Noir
  - Sepia
  - Sketch
  - Emboss
  - Posterize
  - Pixelate
  - Solarize
  - Vintage
  - Cartoon
  - Neon Glow
  - Blur

## Setup Instructions

1. Make sure you have Python 3.8+ installed on your system.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python back.py
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Click "Select your image" to choose an image from your computer
2. Select an art style from the dropdown menu
3. Click "Generate Art" to process the image
4. Once processing is complete, you can view the result and download it

## Technical Details

- Backend: Python with Flask
- Image Processing: Pillow (PIL)
- Frontend: HTML, CSS, JavaScript
- CORS enabled for API requests

## Error Handling

The application includes error handling for:
- Invalid image files
- Missing parameters
- Processing errors
- Network issues

## License

This project is open source and available under the MIT License. 