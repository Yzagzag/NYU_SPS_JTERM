import PIL as pil
import PIL.Image as im
import numpy as np
import os.path

max_iters = 10000

center = (-1.752905, 0.01250)
x_scale = 1e-6
pix_width = 1920
pix_height = 1080

progress = 0
progressinc = 5
progresstotal = pix_width*pix_height*progressinc/100
def in_set(c, max_iter=max_iters): 
   global progress
   global progressinc
   global progresstotal
   progress += 1
   if(progress > progresstotal):
      print(progresstotal)
      progresstotal /= pix_width*pix_height/100
      progresstotal += progressinc
      progresstotal *= pix_width*pix_height/100
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
   return -1

def pix_to_comp(coords):
   cx = float(x_scale/pix_width*coords[0] + center[0] - x_scale/2.0)
   cy = float(-x_scale/pix_width*coords[1] + center[1] + x_scale*pix_height / (2.0*pix_width))
   return (cx, cy)

def get_escape_times(the_pix_list):
   
   the_escape_dict = {i: in_set(pix_to_comp(i)) for i in the_pix_list}
   return the_escape_dict

def calibrate_color_map(the_escape_dict, mode='linear', color='cyan'):
   iterations = [i for i in the_escape_dict.values() if i > 0 ]
   log_max = np.log(max(iterations))
   log_min = np.log(min(iterations))
   if(mode=="log"):
      the_color_dict = {i: np.array([0, int(196*np.exp((np.log(i)-log_min)/(log_max-log_min)-1)), int(255*np.exp((np.log(i) - log_min)/(log_max - log_min)-1))]) for i in iterations}
      the_color_dict[-1] = np.array([0, 0, 0])
   if(mode=='linear'):
      if(color=='cyan'):
         the_color_dict = {i:np.array([0, int(i*196/the_max), int(i*255/the_max)]) for i in iterations}
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
   narr = np.asarray(colors_array, dtype=np.uint8)
   mandelpic = im.fromarray(narr, mode='RGB')
   mandelpic.save("6.png")
build_image() 
   

