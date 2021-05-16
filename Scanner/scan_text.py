import io
import os
from google.cloud import vision

cred_path = r'C:\Users\syunn\Documents\Dev\Scanner\my_cred.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('Image/dice.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)

response = client.text_detection(image=image)
for text in response.text_annotations:
    print(text)
