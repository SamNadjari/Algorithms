"""
Sam Nadjari
san7st
Resources:
    https://www.programiz.com/python-programming/methods/list/sort
    Intro to Algorithms, Cormen et. al.
Collaborators:
    Emily Nguyen
"""
import math
import statistics as st

def closest_pair_distance(file_data):
    file_data = file_data[1:]
    # convert file_data to a list of pairs of ints (points)
    points = []
    for line in file_data:
        line = line.replace("\n", "")
        line = line.split(' ')
        line[0] = float(line[0])
        line[1] = float(line[1])
        points.append(line)
    #sort points by x - Python uses timsort, which is O(nlog(n)) 
    X = sorted(points, key=x_coord)
    Y = sorted(points, key=y_coord)
    
    return find_closest_pair(points, X, Y)    

def find_closest_pair(points, X, Y):
    #base case
    if len(points) <= 3:
        return brute(points)
    else:
        #split the lists at the median and recursively find the closest points
        m = len(points)//2
        pL = X[0:m]# = xL
        pR = X[m:]# = xR
        
        #y-sorted lists on the left and right sides of the median
        yL = []
        yR = []
        for point in Y:
            if point[0] < X[m][0]:
                yL.append(point)
            else:
                yR.append(point)
        
        cp_1_left, cp_2_left, deltaL = find_closest_pair(pL, pL, yL)
        cp_1_right, cp_2_right, deltaR = find_closest_pair(pR, pR, yR)
     
    #find the closest pair of points from either side of the median
    delta = min(deltaL, deltaR)
    if delta == deltaL:
        cp_overall_1 = cp_1_left
        cp_overall_2 = cp_2_left
    else:
        cp_overall_1 = cp_1_right
        cp_overall_2 = cp_2_right
        
    #split the lists to find the points within 1 delta of the median
    med = X[len(X)//2][0]
    pStrip = []
    for point in points:
        #if the x-coordinate of the point is within delta of the median, add the point to the strip list
        if (point[0] > med - delta) and (point[0] < med + delta):
            pStrip.append(point)
    
    #creating a list of all points in the strip sorted by y-value
    yStrip = []
    for point in Y:
        if point in pStrip:
            yStrip.append(point)
    
    #check the first 15 points within delta units of each point in the strip to find the closest pair
    if len(yStrip) > 1:
        deltaSplit = distance(yStrip[0], yStrip[1])
        dist = deltaSplit
        cp_1_strip = yStrip[0]
        cp_2_strip = yStrip[1]
        for i in range(len(yStrip)):
            toCheck = 15
            if len(yStrip[i:]) < 15:
                toCheck = len(yStrip[i:])
            for j in range(1,toCheck):
                dist = distance(yStrip[i], yStrip[i+j])
                if dist < deltaSplit:
                    deltaSplit = dist
                    cp_1_strip = yStrip[i]
                    cp_2_strip = yStrip[i+j]
    else:
        deltaSplit = delta + 1
    
    #compare to the closest pair of points found earlier to find the overall closest pair and return
    if deltaSplit < delta:
        return cp_1_strip, cp_2_strip, deltaSplit
    else:
        return cp_overall_1, cp_overall_2, delta

       
#return the x-coordinate of a point
def x_coord(point):
    return point[0]

#return the y-coordinate of a point
def y_coord(point):
    return point[1]

#return the Euclidian distance between 2 points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#find the closest distance between <= 3 points
def brute(points):
    delta = distance(points[0], points[1])
    dist = delta
    cp_1 = points[0]
    cp_2 = points[1]
    if len(points) == 2:
        return cp_1, cp_2, delta
    else: 
        for i in range(len(points)-1):
            for j in range(i+1,len(points)):
                dist = distance(points[i], points[j])
                if dist < delta:
                    delta = dist
                    cp_1 = points[i]
                    cp_2 = points[j]
        return cp_1, cp_2, delta

  


