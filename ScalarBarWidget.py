#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# by Panos Mavrogiorgos, email : pmav99 >a< gmail

import vtk
import vtk.util.numpy_support as VN
import numpy as np


def get_program_parameters():
    import argparse
    description = 'Scalar bar widget.'
    epilogue = '''
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='uGridEx.vtk.')
    args = parser.parse_args()
    return args.filename


def colormap():
    colors = vtk.vtkNamedColors()

    # colors.SetColor('bkg', [0.1, 0.2, 0.4, 1.0])

    # The source file
    file_name = get_program_parameters()

    #the name of data array which is used in this example
    daryName = 'v02'#'tev'  'v03' 'prs' 


    # Read the source file.
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_name)
    reader.Update()  # Needed because of GetScalarRange
    print(reader)
    output = reader.GetOutput()
    scalar_range = output.GetScalarRange()

    # specify the data array in the file to process
    reader.GetOutput().GetPointData().SetActiveAttribute(daryName, 0)

    # convert the data array to numpy array and get the min and maximum valule
    dary = VN.vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars(daryName))
    dMax = np.amax(dary)
    dMin = np.amin(dary)
    dRange = dMax - dMin
    print("Data array max: ", np.amax(dary))
    print("Data array min: ", np.amin(dary))


    # Create a custom lut. The lut is used both at the mapper and at the
    # scalar_bar
    lut = vtk.vtkLookupTable()
    lut.SetTableRange(dMin,dMax)
    lut.Build()

    

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(output)
    mapper.SetScalarRange(scalar_range)
    mapper.SetLookupTable(lut)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('bkg'))

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(300, 300)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # create the scalar_bar
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetOrientationToHorizontal()
    scalar_bar.SetLookupTable(lut)

    # create the scalar_bar_widget
    scalar_bar_widget = vtk.vtkScalarBarWidget()
    scalar_bar_widget.SetInteractor(interactor)
    scalar_bar_widget.SetScalarBarActor(scalar_bar)
    scalar_bar_widget.On()

    interactor.Initialize()
    render_window.Render()
    renderer.GetActiveCamera().SetPosition(-6.4, 10.3, 1.4)
    renderer.GetActiveCamera().SetFocalPoint(1.0, 0.5, 3.0)
    renderer.GetActiveCamera().SetViewUp(0.6, 0.4, -0.7)
    render_window.Render()
    interactor.Start()


# if __name__ == '__main__':
#     colormap()