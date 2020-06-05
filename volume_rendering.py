import vtk
import json
import numpy as np
import vtk.util.numpy_support as VN
from pprint import pprint


# This template is going to show a slice of the data

# the data used in this example can be download from
# http://oceans11.lanl.gov/deepwaterimpact/yA31/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_49275.vti 

#setup the dataset filepath (change this file path to where you store the dataset)
filename = '/home/tony/Desktop/DV_homework/homework5/pv_insitu_300x300x300_30068.vti.part'

#the name of data array which is used in this example
daryName = 'tev' #'v02' 'v03' 'prs' 

# for accessing build-in color access
colors = vtk.vtkNamedColors() 

# Create the renderer, the render window, and the interactor. The
# renderer draws into the render window, the interactor enables
# mouse- and keyboard-based interaction with the data within the
# render window.
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Set a background color for the renderer and set the size of the
# render window.
ren1.SetBackground(51/255, 77/255, 102/255)


# data reader
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(filename)
reader.Update()

# specify the data array in the file to process
reader.GetOutput().GetPointData().SetActiveAttribute(daryName, 0)

# convert the data array to numpy array and get the min and maximum valule
dary = VN.vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars(daryName))
dMax = np.amax(dary)
dMin = np.amin(dary)
dRange = dMax - dMin
print("Data array max: ", np.amax(dary))
print("Data array min: ", np.amin(dary))

########## setup color map ###########
# Now create a lookup table that consists of the full hue circle
# (from HSV).
hueLut = vtk.vtkLookupTable()
hueLut.SetTableRange(dMin, dMax)
# hueLut.SetHueRange(0, 1)  #comment these three line to default color map, rainbow
# hueLut.SetSaturationRange(1, 1)
# hueLut.SetValueRange(1, 1)
hueLut.Build()  # effective built

# An outline provides context around the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
outlineData.Update()

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("Black"))

# Define color transfer function
funcColor = vtk.vtkColorTransferFunction()

# Define scalar opacity transfer function
funcOpacityScalar = vtk.vtkPiecewiseFunction()

# Define gradient opacity transfer funciton
funcOpacityGradient = vtk.vtkPiecewiseFunction()

funcOpacityGradient.AddPoint(1,0.0)
funcOpacityGradient.AddPoint(5,0.1)
funcOpacityGradient.AddPoint(100,1.0)

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
#pprint(data)
nOpaPoint = int( len( data[0]['Points'])/4 ) # number of opacity function control point
for i in range( nOpaPoint ):
    dtValue = data[0]['Points'][i*4]
    opaValue = data[0]['Points'][i*4+1]
    funcOpacityScalar.AddPoint(dtValue,opaValue)
    print('opacity control point: ', i, ': ', dtValue, opaValue)
nRgbPoint= int( len( data[0]['RGBPoints'] ) / 4 ) # number of the color map control point
for i in range( nRgbPoint ):
    dtValue = data[0]['RGBPoints'][i*4]
    r = data[0]['RGBPoints'][i*4+1]
    g = data[0]['RGBPoints'][i*4+2]
    b = data[0]['RGBPoints'][i*4+3]
    funcColor.AddRGBPoint(dtValue, r,g,b)
    print('rgb control point: ', i, ': ', dtValue, r, g, b)

# after load the control points from opacity function and color map, 
# You can use them to setup you transfer function in VTK

# Volume Properties
propVolume = vtk.vtkVolumeProperty()
propVolume.ShadeOff()
propVolume.SetColor(funcColor)
propVolume.SetScalarOpacity(funcOpacityScalar)
propVolume.SetGradientOpacity(funcOpacityGradient)
propVolume.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and 
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(propVolume)

ren1.AddVolume(volume)
ren1.SetBackground(colors.GetColor3d("Wheat"))
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()

# ren1.Render()

renWin.SetSize(600, 600)
renWin.Render()

iren.Start()


#### Volume Rendering
# vtkVolumeRayCastMapper
# funcRayCast = vtk.vtkVolumeRayCastCompositeFunction()
# funcRayCast.SetCompositeMethodToClassifyFirst()

# mapperVolume = vtk.vtkVolumeRayCastMapper()
# mapperVolume.SetVolumeRayCastFunction(funcRayCast)
