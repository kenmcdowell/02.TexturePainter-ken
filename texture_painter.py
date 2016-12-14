'''Renders text from a CSV file to textures
and applies them to multiple objects.

Use snippets...
import os, sys; sys.path.append(os.path.dirname(bpy.data.filepath)); import texture_painter
import importlib; importlib.reload(texture_painter); texture_painter.go()
import codecs
codecs.open('backers_10.csv', 'r', 'utf-8-sig')

'''
import codecs
import os
import bpy
import csv
from PIL import Image, ImageDraw, ImageFont

def get_backers(csv_filename):
    with codecs.open(csv_filename, 'r', 'utf-8-sig') as stream: #only keeps the file open while reading, then closes it
        iterable = csv.reader(stream) # Python iterable object using csv method to read line by line
        header = next(iterable) #next method gets only the header row
        for row in iterable: #goes thru ea row that the stream generates
            backer = dict(zip(header, row)) #uses a python dict object to store row as name, value pairs using the header row as names
            #zip function interleaves values from the tuple
            yield backer  # this is sorta like return, but does it per row
# changed this thing againg again again
def render_text_to_file(text_to_render, filename):
    # create image file
    kenImage = Image.new('RGB', (512, 64), color=(0, 0, 0))
    # write text to Image using ImageFont by creating an imageDraw object
    kendraw = ImageDraw.Draw(kenImage) # draw object created
    kenfont = ImageFont.truetype("Arial.ttf", 50) # font object created referring to ttf file that's in our project directory
    # draw text to the image
    kendraw.text((5,5), text_to_render, fill=(255, 255, 255), font=kenfont) # using the text method on the object of type ImageDraw that we created
    # save file
    #imagefilename = projectfilepath + "/imagefolder/" + num + ".png"
    #imagefilename = "10.png"
    #kenImage.save(imagefilename)
    #some chagned comments in here to see if GitHub is watching
    kenImage.save(filename)

def read_csv():
    projectfilepath = os.path.dirname(bpy.data.filepath)
    for backer in get_backers(projectfilepath + '/backers_10.csv'):
        filename = projectfilepath + '/texture_cache/' + backer['Number'] + '.png'
        text_to_render = backer['Name'] + ", " + backer['Country']
        render_text_to_file(text_to_render, filename)
        #render_text_to_file("William", "09", projectfilepath)
        #render_text_to_file("It worked!", "10", projectfilepath)
        #print(backer)
    #print(get_backers(projectfilepath + '/backers_10.csv'))

def throw_invalid_selection():
    if len(bpy.context.selected_objects) == 0:
        raise Exception("Please select exactly one prototype object.")
    if len(bpy.context.selected_objects) > 1:
        raise Exception("Please select exactly one prototype object.")

def create_plaque(prototype, offset):
    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":offset}) #this line uses command that mirrors Shift-D duplicate function in the Blender UI
    #bpy.context.selected_objects[0].select = False #this would work, but nothing is returned back to the calling method, could we use yield?
    new_plaque = bpy.context.selected_objects[0] #in the code this has to be assigned to an object rather than just executed immediately as in the console
    new_plaque.select = False #This is to unselect the newly created plaque
    return new_plaque

def go():
    print("Texture Painter starting up.")
    #read_csv() # this format will call the method, i.e. as a subroutine
    throw_invalid_selection()
    print("Exactly one prototype object selected")

    # pass in selected object
    prototype = bpy.context.selected_objects[0]
    create_plaque(prototype, (0,1,0))
