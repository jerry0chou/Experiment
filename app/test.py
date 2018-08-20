import time
tu=(1381419600,1)
print(type(1381419600))
timeStamp=tu[0]
timeArray=time.localtime(timeStamp)
mydatetime=time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
print("mydatetime:",mydatetime)