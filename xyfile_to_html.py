import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_interactions import ioff, panhandler, zoom_factory
import peakutils
import mpld3
import tkinter
import easygui
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

print("Please open the xy file.")
try:      
      filename=askopenfilename()
      ext=filename.split(".")
      if ext[1] == "xy":
            data=pd.read_csv(filename, delimiter=' ', header=None)
      #elif ext[1] == "txt":
      #      data=pd.read_csv(filename, delimiter=',', header=None) 
      #      data=data[[1,2]]
      #      data=data.rename(columns={1:0, 2:1})
      else:      
            #print("Only xy or txt files please.")
            print("Only xy files please.")
            i=0
            while i in range (0,3):
                  if ext[1] != "xy":
                  #if ext[1] != "xy" and ext[1] != "txt":
                        filename=askopenfilename()
                        ext=filename.split(".")
                        i=i+1
                  else:
                        break
except Exception as error:
      print("Needs to be a file.")

print("Please select the top _ peaks for labeling. (Answers as integers only)")
try:
      topx=int(input())
except Exception as error:
      i=0
      while i in range (0,3):
            print("Needs to be an integer")
            topx=input()
            if isinstance(int(topx), int) is True:
                  break
            else:
                  i=i+1            			
      if isinstance(int(topx), int) is False:    
            print("Top 100 will be used")
            topx=100
      else:
            topx=int(topx)
	
topPeaks=data.nlargest(topx, 1)

stopPeaks=topPeaks.sort_values([0])
stopPeaks=stopPeaks.reset_index(drop=True)
ClstopPeaks=[]
max=stopPeaks[1].max()
topx_1=topx-2
topx_2=topx-3
topx_3=topx-4
i=0
while i in range(len(stopPeaks[0])-1) and i<(topx-1):
      currentx=stopPeaks[0][i]
      currenty=stopPeaks[1][i]
      nexty=stopPeaks[1][i+1]
      if i<=(topx_2):
            nextnexty=stopPeaks[1][i+2]
      if i<=(topx_3):
            nextnextnexty=stopPeaks[1][i+3]
      if stopPeaks[0][i+1]-stopPeaks[0][i]<0.5 and stopPeaks[0][i+2]-stopPeaks[0][i+1]<0.5:
           while stopPeaks[0][i+1]-stopPeaks[0][i]<0.5 and currenty<=max and i<(topx_3):
                 if currenty>nexty and currenty>nextnexty:
                      max=currenty
                 elif currenty<nexty and nexty>nextnexty:
                      max=nexty
                 elif currenty<nexty and nexty<nextnexty:
                      max=nextnexty
                 elif currenty<nexty and nextnexty<nextnextnexty:
                      max=nextnextnexty
                 if max==stopPeaks[1][i]:
                     break
                 else:
                     i=i+1
                     currenty=stopPeaks[1][i]
                     nexty=stopPeaks[1][i+1]
                     nextnexty=stopPeaks[1][i+2]
                     nextnextnexty=stopPeaks[1][i+3]
           ClstopPeaks.append(stopPeaks[0][i])
           ClstopPeaks.append(stopPeaks[1][i])
           max=stopPeaks[1].max()
      elif stopPeaks[0][i+1]-stopPeaks[0][i] <0.5 and stopPeaks[0][i+2]-stopPeaks[0][i+1]>0.5 and currenty>nexty:
           ClstopPeaks.append(stopPeaks[0][i])
           ClstopPeaks.append(stopPeaks[1][i])
           i=i+1
      elif stopPeaks[0][i+1]-stopPeaks[0][i] <0.5 and stopPeaks[0][i+2]-stopPeaks[0][i+1]>0.5 and currenty<nexty:
           ClstopPeaks.append(stopPeaks[0][i+1])
           ClstopPeaks.append(stopPeaks[1][i+1])
           i=i+1
      i=i+1
      if stopPeaks[0][i] - currentx < 0.5:
            while stopPeaks[0][i] - currentx < 0.5 and i<=(topx-2):
                  i=1+i
      if stopPeaks[0][i+1]-stopPeaks[0][i]>=0.5 and i<=topx-1:
            ClstopPeaks.append(stopPeaks[0][i])
            ClstopPeaks.append(stopPeaks[1][i])
      i=i+1

label_x=ClstopPeaks[::2]
label_y=ClstopPeaks[1::2]

x=np.array(data[0])
y=np.array(data[1])


xl=np.array(label_x)
yl=np.array(label_y)

xl_text=xl-20
yl_text=yl

with plt.ioff():
    figure, axis = plt.subplots()

plt.xlabel("m/z", fontsize=20)
plt.ylabel("Intensity", fontsize=20)
print("Please type title for plot.")
title=input()
plt.title(title, fontsize=30)
plt.plot(x, y, linewidth=0.5)

for xy in zip(xl, yl):
      axis.annotate('(%s, %s)' % xy, xy=xy, xycoords='data', textcoords='data', fontsize=10)

axis.grid()

disconnect_zoom = zoom_factory(axis)
pan_handler = panhandler(figure)
plt.show()

html_str=mpld3.fig_to_html(figure)
print("Please choose a directory to save the plot.")
path_to_save=askdirectory()
path_to_save_and_file=path_to_save+"/"+title+".html"
html_file=open(path_to_save_and_file, "w")
html_file.write(html_str)
html_file.close()
