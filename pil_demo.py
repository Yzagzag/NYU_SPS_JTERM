import PIL as pil
import PIL.Image as im
import numpy as np

max_iters = 10000

center = (-1.752905, 0.01250)
x_scale = 1e-6
pix_width = 1920
pix_height = 1080

# some parameters so I get a nice little progress bar. Note the arithmetic I 
# do here - this avoids magic numbers below and saves on extra computations 
# during each pixel's computation.
computed_pixels = 0
computed_percent = 0
percent_increment = 2
progress_bar_len = 50
total_pixels = pix_width*pix_height
pix_per_increment = int(total_pixels / 50)


def in_set(c, max_iter=max_iters): 
   # Tell python about these external variables in a way that allows this
   # function to change their values in a way that persists after this
   # function completes.
   
   global computed_pixels
   global computed_percent
   computed_pixels += 1
   
   if(computed_pixels == pix_per_increment):
      computed_percent += percent_increment
      computed_pixels = 0
      # Double slash (//) in python 3 forces the result of division to be
      # an integer.
      hashmarks = computed_percent*progress_bar_len//100

      # Note the line splitting here: it's good style to break up lines that
      # would otherwise be too long!      
      print("Progress: " + str(computed_percent) + "%" + 
         " "*(4-len(str(computed_percent))) +  "[" + "#"*hashmarks + 
         "-"*(progress_bar_len-hashmarks) + "]")
   n=1
   rez_iter = c[0]
   imz_iter = c[1]
   temp_iter = 0.0
   while(n<max_iter):
      temp_iter = 2.0*rez_iter*imz_iter + c[1]
      rez_iter = rez_iter*rez_iter - imz_iter*imz_iter + c[0]
      imz_iter = temp_iter
      if(rez_iter*rez_iter + imz_iter*imz_iter > 4.0):
         return n
      n += 1

   # if point never escapes, return -1 to not conflict with color palette

   return -1

def pix_to_comp(coords):
   cx = float(x_scale/pix_width*coords[0] + center[0] - x_scale/2.0)
   cy = float(-x_scale/pix_width*coords[1] + center[1] + x_scale*pix_height / (2.0*pix_width))
   return (cx, cy)

def get_escape_times(the_pix_list):
   
   # Here I've used a unique syntax to python: a dictionary comprehension.
   # You can also do list comprehensions, and the syntax is:
   # [funct(element) for element in iterable]
   # The result is a list made by applying the function funct to each
   # element of iterable in sequence. Iterables are commonly lists but 
   # more general than that. A non-list iterable that you may be familiar 
   # with is the output of range().

   the_escape_dict = {i: in_set(pix_to_comp(i)) for i in the_pix_list}
   return the_escape_dict

def calibrate_color_map(the_escape_dict, mode='linear', color='cyan'):
   iterations = [i for i in the_escape_dict.values() if i > 0 ]
   log_max = np.log(max(iterations))
   log_min = np.log(min(iterations))
   
   if(mode=="log"):
      the_color_dict = {i: np.array([0, 
         int(196*np.exp((np.log(i)-log_min) /(log_max-log_min)-1)), 
         int(255*np.exp((np.log(i) - log_min)/(log_max - log_min)-1))]) 
         for i in iterations}
      the_color_dict[-1] = np.array([0, 0, 0])
   
   if(mode=='linear'):
      if(color=='cyan'):
         the_color_dict = {i:np.array([0, 
            int(i*196/the_max), 
            int(i*255/the_max)]) 
            for i in iterations}
         the_color_dict[-1] = np.array([0, 0, 0])
   
   return the_color_dict

def build_image():

   pix_list = [(i,j) for i in range(pix_height) for j in range(pix_width)]
   escape_dict = get_escape_times(pix_list)
   palette_dict = calibrate_color_map(escape_dict, mode='log')
   final_colors_dict = {i:palette_dict[escape_dict[i]] for i in escape_dict}

   colors_array = np.zeros(shape=(pix_height, pix_width, 3))

   for i in range(pix_height):
      for j in range(pix_width):
         colors_array[i,j] = final_colors_dict[(i,j)]
   # Don't forget to convert array to data type uint8!!!)
   narr = np.asarray(colors_array, dtype=np.uint8)
   mandelpic = im.fromarray(narr, mode='RGB')

   # im.save() is very aggressive - if 6.png already exists, it will be
   # overwritten!!! One way to be safe is to always move output you care about
   # to another folder once it's created. A more automated way would be to
   # check if the filename exists using the os.path module and a try... catch
   # statement!

   mandelpic.save("6.png")
build_image() 
   

