import vtk
import vtk.util.numpy_support as VN
import numpy as np

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
aRenderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(aRenderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Set a background color for the renderer and set the size of the
# render window.
aRenderer.SetBackground(51/255, 77/255, 102/255)
renWin.SetSize(600, 600)

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

########## create plane (slice)  ###########
# xy plane
xyColors = vtk.vtkImageMapToColors()
xyColors.SetInputConnection(reader.GetOutputPort())
xyColors.SetLookupTable(hueLut)
xyColors.Update()

xy = vtk.vtkImageActor()
xy.GetMapper().SetInputConnection(xyColors.GetOutputPort())
######### TODO: fill up the parameter in the following line to slice the plance at xy plane #####
xy.SetDisplayExtent(0,300,0,300,140,300) 

# It is convenient to create an initial view of the data. The
# FocalPoint and Position form a vector direction. Later on
# (ResetCamera() method) this vector is used to position the camera
# to look at the data in this direction.
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, -1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()
aCamera.Azimuth(30.0)
aCamera.Elevation(30.0)

# Actors are added to the renderer.
aRenderer.AddActor(outline)
aRenderer.AddActor(xy)

# An initial camera view is created.  The Dolly() method moves
# the camera towards the FocalPoint, thereby enlarging the image.
aRenderer.SetActiveCamera(aCamera)

# Calling Render() directly on a vtkRenderer is strictly forbidden.
# Only calling Render() on the vtkRenderWindow is a valid call.
renWin.Render()

aRenderer.ResetCamera()
aCamera.Dolly(1.5)

# Note that when camera movement occurs (as it does in the Dolly()
# method), the clipping planes often need adjusting. Clipping planes
# consist of two planes: near and far along the view direction. The
# near plane clips out objects in front of the plane; the far plane
# clips out objects behind the plane. This way only what is drawn
# between the planes is actually rendered.
aRenderer.ResetCameraClippingRange()

# Interact with the data.
renWin.Render()
iren.Initialize()
iren.Start()


