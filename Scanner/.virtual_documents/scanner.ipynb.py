# get_ipython().run_line_magic("%writefile", " scan_text.py")
import io
import os
from google.cloud import vision

cred_path = r'C:\Users\syunn\Documents\Dev\Scanner\my_cred.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

client = vision.ImageAnnotatorClient()

file_name = os.path.abspath('Image/dice.jpg')

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
type(response.text_annotations[0])
# for text in response.text_annotations:
#     print(text.description)


# get_ipython().run_line_magic("%writefile", " add_frame.py")
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


import os
import io
from PIL import Image, ImageDraw
from google.cloud import vision

def detect_crop_hints(path,output_filename):
    """Detects crop hints in an image."""
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    crop_hints_params = vision.CropHintsParams(aspect_ratios=[1])
    image_context = vision.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    for hint in hints:
        box = [(vertex.x, vertex.y) for vertex in hint.bounding_poly.vertices]
        draw.line(box + [box[0]], width=2, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
    im.save(output_filename)
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        
        
if __name__ == "__main__":
    cred_path = r'C:\Users\syunn\Documents\Dev\Scanner\my_cred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
    image = "Image/sample1.jpg"
    output = "Image/sample1_croped.jpg"
    detect_crop_hints(image,output)


get_ipython().run_cell_magic("writefile", " scan.py", """
import os
import io
from PIL import Image, ImageDraw
from google.cloud import vision

class Scan():
    image_path = ""
    output_path = ""
    dictionary = []

    def __init__(self,image_path=None,output_path=None,dictionary=[]):
        self.image_path = image_path
        self.output_path = output_path
        self.dictionary = dictionary
        
    def get_annotations(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image_path, 'rb') as image:
            content = image.read()
        vision_image = vision.Image(content=content)
        response = client.text_detection(image=vision_image)
        return response.text_annotations
    
    def search_dictionary(self,annotations=None):
        descriptions = [data.description for data in annotations]
        flags = [False] * len(descriptions)
        for i,text in enumerate(descriptions):
            for j in range(len(descriptions) - i - 1):
                for word in self.dictionary:
                    if text == word:
                        for k in range(j+1):
                            flags[i+k] = True
                text += descriptions[i+j+1]
        return flags
    
    def redraw_image(self,annotations=None,flags=[]):
        vertices = [data.bounding_poly for data in annotations]
        im = Image.open(self.image_path)
        draw = ImageDraw.Draw(im)
        for i, flag in enumerate(flags):
            if flag == True:
                box = [(vertices[i].vertices[2].x, vertices[i].vertices[2].y), (vertices[i].vertices[3].x, vertices[i].vertices[3].y)]
                draw.line((box[0], box[1]), width=2, fill='#00ff00')
        try:
            im.save(self.output_path)
            return True
        except:
            return False
        
if __name__ == "__main__":
    
    cred_path = r'C:\Users\syunn\Documents\Dev\Scanner\my_cred.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path

    scan = Scan(image_path="Image/sample1.jpg",output_path="Image/sample1_scan.jpg",dictionary=["Ž_","‚±‚Ì•\Ž¦","ˆÀ“¡"])
    annotations = scan.get_annotations()
    flags = scan.search_dictionary(annotations)
    if scan.redraw_image(annotations,flags):
        print("scan is completed.")
    else:
        print("scan is failed")
""")



