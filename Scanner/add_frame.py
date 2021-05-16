import io
import os
from PIL import Image, ImageDraw
from google.cloud import vision

def read_img(image_file):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(image_file)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    return response.text_annotations

def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.rectangle(box + [box[0]], fill=(0,255,0))
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
    im.save(output_filename)
        
if __name__ == "__main__":
    cred_path = r'C:\Users\syunn\Documents\Dev\Scanner\my_cred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
    image = "Image/dice.jpg"
    output = "Image/dice_flame.jpg"
    highlight_faces(image,read_img(image),output)
