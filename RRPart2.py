import sys
#import matplotlib.pyplot as plt
from math import pi , acos , sin , cos
import time
import queue as Q
from tkinter import *

def distance(y1,x1, y2,x2):
   y1 = float(y1)
   x1 = float(x1)
   y2 = float(y2)
   x2 = float(x2)
   dist = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   if sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) >1:
      return 23
   else:
      return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * dist
   
def createCities():
   cityFile = open("romCities.txt", "r")
   myList = cityFile.readlines()
   cityToCode = {}
   for i in myList:
      city = i[2:len(i)-1]
      if city == "Zerin":
         city = "Zerind"
      cityToCode[city] = i[0:1]
   return cityToCode

def createLatLongs():
   latLongFile = open("romLatLong.txt", "r")
   myList = latLongFile.readlines()
   latLong = {}
   for i in myList:
      code = i[0:1]
      lat = i[2:9]
      long = i[10:len(i)-1]
      latLong[code] = (lat, long)
   latLong["Z"] = (46.6167,21.5167)
   return latLong
   
def makeMyEdges():
   edgeFile = open("romEdges.txt", "r")
   myList = edgeFile.readlines()
   edges = {}
   for i in myList:
      code = i[0:1]
      if code == "Z":
         code2 = str(i[2:])
      else:
         code2 = str(i[2:len(i)-1])
      if code2 != "":
         if code in edges.keys():
            edges[code].append(code2)
         else:
            edges[code] = [code2]
         if code2 in edges.keys():
            edges[code2].append(code)
         else:
            edges[code2] = [code]
   edges["U"].append("V")
   edges["V"].append("U")
   return edges
   
def findDistance(code1, code2):
   list3 = Q.PriorityQueue()
   citiesList = edges[code1]
   for i in citiesList:
      list3.put((distance(llDict[code1][0], llDict[code1][1], llDict[i][0], llDict[i][1]), code1, i))
      #print((distance(llDict[code1][0], llDict[code1][1], llDict[i][0], llDict[i][1])))
   trackDict = {}
   while not list3.empty():
      tupRem = list3.get()
      #print("removed" + str(tupRem))
      if tupRem[2] == code2:
         return tupRem[0]
      else:
         word = tupRem[2]
         citiesList = edges[word]
         #print("cities" + str(citiesList))
         for i in citiesList:
            if i != tupRem[1] and i not in trackDict:
               disti = distance(llDict[word][0], llDict[word][1], llDict[i][0], llDict[i][1])
               list3.put((disti + tupRem[0], word, i))
         trackDict[word] = (citiesList[len(citiesList)-1],disti)

city1 = sys.argv[1]
city1 = city1.replace("_"," ")
city2 = sys.argv[2]
city2 = city2.replace("_"," ")
if city1 == city2:
   print("The cities you entered are the same")
else:
   cityToCode = createCities()
   #keys are cities and values are codes
   llDict = createLatLongs()
   #keys are codes and values are lat long tuples
   edges = makeMyEdges()
   #keys are first node and values are second node with distance between them
   code1 = cityToCode[city1]
   code2 = cityToCode[city2]
   sum = 0.0
   dist = int(findDistance(code1, code2))
   print("Distance between "+ str(city1) + " and " + str(city2) + " is " + str(dist) + " miles")
   for i in edges:
      for x in edges[i]:
         sum += distance(llDict[x][0], llDict[x][1], llDict[i][0], llDict[i][1])
   print("Sum of all edges is: " + str(sum/2) + " miles")

#code for tkinter
root = Tk()
canvas= Canvas(root,width = 1400,height = 500,bg="white")
canvas.postscript(rotate=False)
dc = canvas.create_text(1, 100, text="")
canvas.scale(dc, 360, 240, 2, 2)
canvas.pack()

#width = 1400
#height = 500
#now actually have to make nodes
#table = {"A": (100,100), "B": (900,400),"C": (500, 400),"D": (300,400),"E": (1250,400),"F": (600,200),"G": (900,450),
#"H": (1200,350),"I": (1100,100),"L": (300,300),"M": (300,350),"N": (900,50),"O": (300,10),"P": (700,325),"R": (450,250),
#"S": (400,170),"T": (100,250),"U": (1000,350),"V": (1150,200),"Z":(200,60)}

#cities = {"A":"Arad", "B":"Bucharest","C":"Craiova","D":"Drobeta","E":"Eforie",
#"F":"Fagaras","G":"Giurgiu","H": "Harsova","I": "Iasi","L": "Lugoj","M": "Mehadia",
#"N": "Neamt","O": "Oradea","P": "Pitesti","R": "Ramnicu Valcea","S": "Sibiu",
#"T": "Timisoara","U" :"Urziceni","V": "Vaslui","Z" :"Zerind"}

# for i in edges:
#    canvas.create_oval(table[i][0], table[i][1], table[i][0]+20, table[i][1]+20)
#    canvas.create_text(table[i][0]+10, table[i][1]+10, text=i)
# 
# for i in edges:
#    for x in edges[i]:
#       canvas.create_line(table[i][0], table[i][1], table[x][0], table[x][1])   
#       distee = round(distance(llDict[x][0], llDict[x][1], llDict[i][0], llDict[i][1]),1)
#       canvas.create_text((table[i][0]+table[x][0])/2 + 10, (table[i][1]+table[x][1])/2 + 10, text = distee)

#width = 1400
#height = 500

#range lat--> 43.9008-47.1569
#range long--> 21.2300-28.6333

width_scale = 1000/(28.6333-21.2300)
height_scale = 300/(47.1569-43.9008)
print(width_scale)
print(height_scale)

for i in edges:
   height = (float(llDict[i][0])-43.9008)
   width = (float(llDict[i][1])-21.2300)
   height = 400-height*height_scale
   width = width*width_scale
   canvas.create_oval(width, height, width+20,height+20)
   canvas.create_text(width+10,height+10,text=i)
   for x in edges[i]:
      height2 = (float(llDict[x][0])-43.9008)
      width2 = (float(llDict[x][1])-21.2300)
      height2 = 400-height2*height_scale
      width2 = width2*width_scale
      canvas.create_line(width, height, width2, height2)   
      distee = round(distance(llDict[x][0], llDict[x][1], llDict[i][0], llDict[i][1]),1)
      canvas.create_text((width+width2)/2, (height+height2)/2,text = distee)
 
root.mainloop()