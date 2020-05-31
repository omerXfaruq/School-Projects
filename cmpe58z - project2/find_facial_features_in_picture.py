from PIL import Image, ImageDraw
import face_recognition
import sys

if len(sys.argv)!=2:
    print("Please give photo name as argument while running\nExiting now")
    sys.exit(1)

fileName=sys.argv[1]

# Load the image file into a numpy array
image = face_recognition.load_image_file(fileName)

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)
print("I found {} face landmark(s) in this photograph.".format(len(face_landmarks_list)))


#Find all faces in the picture using cnn based model
face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
print("I found {} face(s) in this photograph.".format(len(face_locations)))

# Create a PIL imagedraw object so we can draw on the picture
pil_image = Image.fromarray(image)
d = ImageDraw.Draw(pil_image)

#Draw landmarks
for face_landmarks in face_landmarks_list:

    # Print the location of each facial feature in this image
#    for facial_feature in face_landmarks.keys():
        #print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

    # Let's trace out each facial feature in the image with a line!
    for facial_feature in face_landmarks.keys():
        #print(face_landmarks[facial_feature],width=5)
        d.line(face_landmarks[facial_feature], width=5)

#Draw red boxes
for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    d.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=3,fill=128) 
    #face_image = image[top:bottom, left:right]
    #pil_image = Image.fromarray(face_image)
    #pil_image.show()

# Show the picture
pil_image.show()
