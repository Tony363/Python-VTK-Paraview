import json
from pprint import pprint

# How to save transfer function from Paraview
# In 'color mapp editor', click the button 'Save to present' (a folder icon with a green arrow)
# A window 'Save present option' will pop out, make sure 'Save opatities' is checked. Then click 'OK'
# A window 'Choose present' will pop out, click 'Export' and set the transfer function to a .json file

# # load transfer function from paraview
# paraview transfer function assume the data range are 0 to 1.
# when you setup the trasnfer function in vtk, you have to rescale it to the data range of the dataset
json_data=open('/home/tony/Desktop/DV_homework/homework5/cool_warm.json')
data = json.load(json_data)
json_data.close()
# pprint(data)
nOpaPoint = int( len( data[0]['Points'])/4 ) # number of opacity function control point
for i in range( nOpaPoint ):
    dtValue = data[0]['Points'][i*4]
    opaValue = data[0]['Points'][i*4+1]
    print('opacity control point: ', i, ': ', dtValue, opaValue)
nRgbPoint= int( len( data[0]['RGBPoints'] ) / 4 ) # number of the color map control point
for i in range( nRgbPoint ):
    dtValue = data[0]['RGBPoints'][i*4]
    r = data[0]['RGBPoints'][i*4+1]
    g = data[0]['RGBPoints'][i*4+2]
    b = data[0]['RGBPoints'][i*4+3]
    print('rgb control point: ', i, ': ', dtValue, r, g, b)

# after load the control points from opacity function and color map, 
# You can use them to setup you transfer function in VTK