# -*- coding: utf-8 -*-

import math as m
import matplotlib.pyplot as plt

#variables
MIDI_NOTES = 127
angle = 0
slope = 0
length = 120
angle_frac = (6 * m.pi)/length
slope_frac = MIDI_NOTES/length

#functions
f_x = []
g_x = []
h_x = []

for i in range (length):
    f_x.append(-slope * abs( m.sin(angle) ) + 30 * m.cos(angle))
    g_x.append(-slope * abs( m.sin(angle + (m.pi/2)) ))
    h_x.append(m.sin(angle))
    angle += angle_frac
    slope += slope_frac


#Combines both lightsounds by higher value of the two
def combine(f_array, s_array):
    combine = []
    
    for i in range(len(f_array)):
        if f_array[i] >= s_array[i]:
            combine.append(f_array[i])
        else:
            combine.append(s_array[i])
    return combine

combination = combine(f_x, g_x)


#Normalizes the data, by choosing local maximum and drawing line between each point
def normalize(array):
    
    #Defines the equation of the line
    def lines(x1, y1, x2, y2):
        return lambda x: ((y2-y1)/(x2-x1)) * (x-x1) +y1
    
    #Function finds the local maximums in the array
    def find_maxima(array):
        #First point of the array is appended
        result = [[0, array[0]]]
        status = 'decrease'
        
        for i in range(len(array)-1):
            #Increasing
            if array[i+1] >= array[i]:
                status = 'increase'
            
            elif status == 'increase' and array[i+1] < array[i]:
                status = 'decrease'
                result.append([i, array[i]])

        #Appends las point of the array   
        result.append([len(array)-1, array[len(array)-1]])
        return result
    
    maximums = find_maxima(array)
    current_line = 0
    
    #Iterates through maximums and draws the line in the while loop
    for i1 in range(len(maximums)-1):
        x1 = maximums[i1][0]
        x2 = maximums[i1+1][0]
        current_line = lines(x1, maximums[i1][1], x2, maximums[i1+1][1])
        
        while x1 != x2:
            array[x1] = current_line(x1)
            x1 += 1
    
    #Returns normalized array
    return array
            
        
#Before normalization
plt.plot(combination)

#Post normalization
normalized = normalize(combination)
plt.plot(combination)

#Test with normal sine function
plt.plot(normalize(h_x))