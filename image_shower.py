import numpy
import echo_reservoir
import transition_matrix_generator
from PIL import Image
import time

class Loader:
    def __init__(self, width, height, alpha, minVal, maxVal, chaosVal):
        # Handles each band seperatly.
        self.red_loaded = False
        self.green_loaded = False
        self.blue_loaded = False
        self.target_width = width
        self.target_height = height
        self.red_band = None
        self.green_band = None
        self.blue_band = None
        self.display_red = None
        self.display_green = None
        self.display_blue = None
        self.alpha = alpha
        self.minVal = minVal
        self.maxVal = maxVal
        self.chaosVal = chaosVal

    def load(self, path):
        image = Image.open(path).resize((self.target_width, self.target_height))
        self.red_band = numpy.asarray(image.getdata(band=0)).reshape((image.width*image.height))/365.0 #0-R, 1-G, 2-B
        self.green_band = numpy.asarray(image.getdata(band=1)).reshape((image.width*image.height))/365.0
        self.blue_band = numpy.asarray(image.getdata(band=2)).reshape((image.width*image.height))/365.0
        self.red_loaded, self.green_loaded, self.blue_loaded = True, True, True

    def reload(self, bandString):
        if "R" in bandString:
            self.red_loaded = True
        if "G" in bandString:
            self.green_loaded = True
        if "B" in bandString:
            self.blue_loaded = True

    def get(self, bandString, timestep):
        if self.red_loaded and "R" in bandString:
            self.red_loaded = False
            return self.red_band
        elif self.blue_loaded and "B" in bandString:
            self.blue_loaded = False
            return self.blue_band
        elif self.green_loaded and "G" in bandString:
            self.green_loaded = False
            return self.green_band
        return numpy.zeros((self.target_width*self.target_height))

    def display_image(self, bandString, image_array):
        if "R" in bandString:
            self.display_red = Image.fromarray((image_array * 365.0).astype(numpy.uint8).reshape(self.target_width, self.target_height)).resize((self.target_width*10, self.target_height*10))
        elif "G" in bandString:
            self.display_green = Image.fromarray((image_array * 365.0).astype(numpy.uint8).reshape(self.target_width, self.target_height)).resize((self.target_width*10, self.target_height*10))
        elif "B" in bandString:
            self.display_blue = Image.fromarray((image_array * 365.0).astype(numpy.uint8).reshape(self.target_width, self.target_height)).resize((self.target_width*10, self.target_height*10))
        if self.display_red is not None and self.display_green is not None and self.display_blue is not None:
            display_image = Image.merge("RGB", (self.display_red, self.display_green, self.display_blue))
            display_image.show()
            display_image.save(str(self.alpha) + "-" + str(self.minVal) + "-" + str(self.maxVal) + "-"+ str(int(time.time())) + "-" + str(self.chaosVal) + ".png") # Save as timestamp to avoid issues
            self.display_red, self.display_green, self.display_blue = None, None, None

"""
alpha = float(input("Set alpha: ")) # probability of connection occuring in adjacency matrix
min_connection = float(input("Set minimum connection strength: "))
max_connection = float(input("Set maximum connection strength: "))
height = int(input("Set image height: "))
width = int(input("Set image width: "))
chaos_factor = float(input("Set chaos factor: ")) # See edge of chaos and logistic map
"""
alpha = 0.0005 # Connectiveness value
# A lower alpha seems to do about the same thing as a higher alpha but with a lower max_connection parameter.
# It therefore seems more prudent to have a lower alpha value and instead change max/min parameters because these
# do not impact computational complexity.
min_connection = 0.0
height = 600 # size of each adjacency matrix is (height*width, height*width) so computation scales poorly for larger
# image sizes - however lower alpha values, which work with standard timestep function for reservoir allows for far larger image resolutions
width = 600
chaos_factor = 3.89321543123134709238745  # this value is supposed to be on the edge of chaos
# edge of chaos value: 3.89321543123134709238745
max_connection = 1.0
# Does each color band separately
adjacency_matrix1 = transition_matrix_generator.generate_adjacency_matrix(alpha, min_connection, max_connection,
                                                                         width, height)
adjacency_matrix2 = transition_matrix_generator.generate_adjacency_matrix(alpha, min_connection, max_connection,
                                                                         width, height)
adjacency_matrix3 = transition_matrix_generator.generate_adjacency_matrix(alpha, min_connection, max_connection,
                                                                         width, height)
loader = Loader(width, height, alpha, min_connection, max_connection, chaos_factor)
reservoir1 = echo_reservoir.echo_reservoir(adjacency_matrix1, lambda t: loader.get("R", t), lambda a: loader.display_image("R", a), width, height, chaos_factor)
reservoir2 = echo_reservoir.echo_reservoir(adjacency_matrix1, lambda t: loader.get("G", t), lambda a: loader.display_image("G", a), width, height, chaos_factor)
reservoir3 = echo_reservoir.echo_reservoir(adjacency_matrix1, lambda t: loader.get("B", t), lambda a: loader.display_image("B", a), width, height, chaos_factor)


while True:
    command = input("Command: ")
    if command == "exit":
        break
    if command == "reload":
        loader.reload("RGB")
    if command == "reload R":
        loader.reload("R")
    if command == "reload G":
        loader.reload("G")
    if command == "reload B":
        loader.reload("B")
    if command == "step":
        reservoir1.do_timestep()
        reservoir2.do_timestep()
        reservoir3.do_timestep()
    if command == "load":
        path = input("Path to image: ")
        loader.load(path)
    if command == "stepseveral":
        count = int(input("How many steps? "))
        for num in range(0, count):
            reservoir1.do_timestep()
            reservoir2.do_timestep()
            reservoir3.do_timestep()
    if command == "reloadstepseveral":
        count = int(input("How many steps? "))
        for num in range(0, count):
            loader.reload("RGB")
            reservoir1.do_timestep()
            reservoir2.do_timestep()
            reservoir3.do_timestep()