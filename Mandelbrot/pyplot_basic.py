###############################################################################
#                                                                             #
#                       THE I M F A M O U S MANDELBROT SET                    #
# These are my solutions,                                                     #
# but please only consult after getting a working version for yourself or     #
# after struggling to the point of wanting to quit.                           #
# Otherwise, you will learn nothing!                                          #
#                                                                             #
###############################################################################

# import packages as neat little names for convenience

import matplotlib as mp
import matplotlib.pyplot as pp
import numpy as np

# I like to define all the magic numbers related to the finished plots up here
# so that I have easy access to changing them later. 

pt_num=101

def iterate_point(x, y, max_iter=100):
   
   # takes the point z=x+iy and finds out if z is in M set. if different 
   # accuracy is desired, set the optional parameter max_iter to 
   # a different value.

   x_iter = x
   y_iter = y
   temp = 0.0
   norm = (x**2 + y**2)**.5

   for it_num in range(1, max_iter):

      # NOTE: temp is a naive way to make sure that you properly update both x_iter
      # and y_iter. iirc python supports dual assignment too, which would look
      # like this: x_iter, y_iter = blah_x, blah_y
      # typically language implemented features like these offer small
      # speedups because the built in functions are optimized with this 
      # syntax in mind.

      temp = 2.0*x_iter*y_iter + y
      x_iter = x_iter**2 - y_iter**2 + x
      y_iter = temp
      norm = (x_iter**2 + y_iter**2)**.5
      if(norm > 2.0):
         return 0   
   return 1

def make_plot():
   
   interval = np.linspace(-2,2,num=pt_num)
   points = [(i,j) for i in interval for j in interval]
   goodpoints = [[],[]]

   for i in points:   
      
      # NOTE: below I use the * operator, which, inside of a function call,
      # automatically expands the contents of the list as sequential arguments
      # to the function. See python docs ss4.7.4 for details.

      if(iterate_point(*i)):
         goodpoints[0].append(i[0])
         goodpoints[1].append(i[1])      

   pp.axes().set_aspect('equal')
   pp.scatter(*goodpoints)   
   pp.savefig("today.jpg")
   
make_plot()
