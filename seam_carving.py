import math
import numpy as np

class SeamCarving:
    
    def __init__(self):
        self.order = []
        
    def append_to_path(self, x):
        self.order.append(x)

    # This method is the one you should implement.  It will be called to perform
    # the seam carving.  You may create any additional data structures as fields
    # in this class or write any additional methods you need.
    # 
    # @return the seam's weight
    def run(self, image):
        rows = len(image[0])
        columns = len(image)
        
        last_pixel_weight = 999999
        last_pixel_x = 0
        min_weight = [[0 for r in range(rows)] for c in range(columns)] 
        weight = 0
        
        #if rows == 1 and columns == 1:
        #    self.append_to_path(0)
        #    return 0
            
        if rows == 1:
            for i in range(columns):
                if i == 0: 
                    min_weight[i][0] = distance(image[i][0], image[i+1][0])
                elif i == columns - 1: 
                    min_weight[i][0] = distance(image[i][0], image[i-1][0])
                else: 
                    min_weight[i][0] = (distance(image[i][0], image[i+1][0]) + distance(image[i][0], image[i-1][0])) / 2
            x = 0
            for i in range(columns): 
                if min_weight[i][0] < min_weight[x][0]:
                    weight = min_weight[i][0]
                    x = i
            self.append_to_path(x)
            return weight

        if columns == 1:
            for j in range(rows):
                self.append_to_path(0)
                if j == 0:
                    weight += distance(image[0][j], image[0][j+1])
                elif j == rows - 1:
                    weight += distance(image[0][j], image[0][j-1])
                else:
                    weight += (distance(image[0][j], image[0][j+1]) + distance(image[0][j], image[0][j-1])) / 2
            return weight
                
        for j in range(rows):
            for i in range(columns):
                min_weight[i][j] = energy(image,i,j)
             
        for j in range(1,rows):
            for i in range(columns):    
                if i == 0:
                    min_weight[i][j] = min_weight[i][j] + min(min_weight[i][j-1], min_weight[i+1][j-1])
                elif i == columns - 1:
                    min_weight[i][j] = min_weight[i][j] + min(min_weight[i-1][j-1], min_weight[i][j-1])
                else:
                    min_weight[i][j] = min_weight[i][j] + min(min_weight[i-1][j-1], min_weight[i][j-1], min_weight[i+1][j-1])
         
        for i in range(columns):
            if min_weight[i][rows-1] < last_pixel_weight:
                last_pixel_weight = min_weight[i][rows-1]
                last_pixel_x = i
        
        self.append_to_path(last_pixel_x)
        weight += min_weight[last_pixel_x][rows-1]

        for i in range(rows-2,-1,-1):
            next_pixel_weight = 999999
            next_pixel_x = 0
            #edge cases 
            if last_pixel_x == 0:
                for j in range(0,2):
                    if min_weight[last_pixel_x+j][i] < next_pixel_weight: 
                        next_pixel_weight = min_weight[last_pixel_x+j][i]
                        next_pixel_x = last_pixel_x+j
            elif last_pixel_x == columns - 1:
                for j in range(-1,1):
                    if min_weight[last_pixel_x+j][i] < next_pixel_weight: 
                        next_pixel_weight = min_weight[last_pixel_x+j][i]
                        next_pixel_x = last_pixel_x+j
            else: 
                for j in range(-1,2):
                    if min_weight[last_pixel_x+j][i] < next_pixel_weight: 
                        next_pixel_weight = min_weight[last_pixel_x+j][i]
                        next_pixel_x = last_pixel_x+j
            self.append_to_path(next_pixel_x)
            last_pixel_x = next_pixel_x
            last_pixel_weight = next_pixel_weight
        
        self.order = self.order[::-1]
            
        return weight

    # Get the seam, in order from top to bottom, where the top-left corner of the
    # image is denoted (0,0).
    # 
    # Since the y-coordinate (row) is determined by the order, only return the x-coordinate
    # 
    # @return the ordered list of x-coordinates (column number) of each pixel in the seam
    #         as an array
    def getSeam(self):
        return self.order
    
def distance(pixel_one, pixel_two):
    return math.sqrt((pixel_two[0]-pixel_one[0]) ** 2 + (pixel_two[1]-pixel_one[1]) ** 2 + (pixel_two[2]-pixel_one[2]) ** 2)
    
def energy(image,i,j):
    if i == 0:
        if 0<j<len(image[0])-1:
            return (distance(image[i][j], image[i+1][j]) + distance(image[i][j], image[i][j+1]) + distance(image[i][j], image[i][j-1])) / 3
        elif j == 0:
            return (distance(image[i][j], image[i+1][j]) + distance(image[i][j], image[i][j+1])) / 2
        else:
            return (distance(image[i][j], image[i][j-1]) + distance(image[i][j], image[i+1][j])) / 2
    elif i == len(image)-1: 
        if 0<j<len(image[0])-1: 
            return (distance(image[i][j], image[i][j+1]) + distance(image[i][j], image[i][j-1]) + distance(image[i][j], image[i-1][j])) / 3
        elif j == 0:
            return (distance(image[i][j], image[i][j+1]) + distance(image[i][j], image[i-1][j])) / 2
        else:
            return (distance(image[i][j], image[i][j-1]) + distance(image[i][j], image[i-1][j])) / 2   
    else:
        if j == 0:
            return (distance(image[i][j], image[i][j+1]) + distance(image[i][j], image[i+1][j]) + distance(image[i][j], image[i-1][j])) / 3
        elif j == len(image[0])-1:
            return (distance(image[i][j], image[i][j-1]) + distance(image[i][j], image[i+1][j]) + distance(image[i][j], image[i-1][j])) / 3
        else:
            return (distance(image[i][j], image[i+1][j]) + distance(image[i][j], image[i][j+1]) + distance(image[i][j], image[i-1][j]) + distance(image[i][j], image[i][j-1])) / 4
    
    