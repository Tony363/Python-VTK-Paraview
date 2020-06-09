#!/usr/bin/env python

import vtk
import json
from pprint import pprint


def main():
    fileName = '/home/tony/Desktop/DV_homework/homework5/pv_insitu_300x300x300_30068.vti'

    colors = vtk.vtkNamedColors()

    # This is a simple volume rendering example that
    # uses a vtkFixedPointVolumeRayCastMapper

    # Create the standard renderer, render window
    # and interactor.
    ren1 = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create the reader for the data.
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(fileName)

    # Create transfer mapping scalar value to color.
    colorTransferFunction = vtk.vtkColorTransferFunction()

    # Create transfer mapping scalar value to opacity.
    opacityTransferFunction = vtk.vtkPiecewiseFunction()

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
        opacityTransferFunction.AddPoint(dtValue,opaValue)
        print('opacity control point: ', i, ': ', dtValue, opaValue)
    nRgbPoint= int( len( data[0]['RGBPoints'] ) / 4 ) # number of the color map control point
    for i in range( nRgbPoint ):
        dtValue = data[0]['RGBPoints'][i*4]
        r = data[0]['RGBPoints'][i*4+1]
        g = data[0]['RGBPoints'][i*4+2]
        b = data[0]['RGBPoints'][i*4+3]
        colorTransferFunction.AddRGBPoint(dtValue, r,g,b)
        print('rgb control point: ', i, ': ', dtValue, r, g, b)

    # after load the control points from opacity function and color map, 
    # You can use them to setup you transfer function in VTK

    # The property describes how the data will look.
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    # The mapper / ray cast function know how to render the data.
    volumeMapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    # The volume holds the mapper and the property and
    # can be used to position/orient the volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    ren1.AddVolume(volume)
    ren1.SetBackground(colors.GetColor3d("Wheat"))
    ren1.GetActiveCamera().Azimuth(45)
    ren1.GetActiveCamera().Elevation(30)
    ren1.ResetCameraClippingRange()
    ren1.ResetCamera()

    renWin.SetSize(600, 600)
    renWin.Render()

    iren.Start()


def get_program_parameters():
    import argparse
    description = 'Volume rendering of a high potential iron protein.'
    epilogue = '''
    This is a simple volume rendering example that uses a vtkFixedPointVolumeRayCastMapper.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='ironProt.vtk.')
    args = parser.parse_args()
    return args.filename


if __name__ == '__main__':
    main()