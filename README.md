 # Python-based project on QML-Pyside2-Pyvista combination
 The source code is based on [Nicanor Romero Venier's project](https://github.com/nicanor-romero/QtVtk) ,
[dao-duc-tung's Python Project](https://github.com/dao-duc-tung/QtVTK-Py) and
[Bakkiaraj Murugesan's Question](https://stackoverflow.com/questions/68517058/can-not-get-pyvista-render-to-work-with-qt-qml-qquickframebufferobject)

## Description
This project provides a solution to render pyvista 3D Visualizations on QML-based UI.

QQuickFramebufferObject(QmlFbo) registers as a QML type so that we can bind the python class to the QML component.
After loading the main QML file, the QmlFbo object will be instantiated. 
After the QmlFbo is created, the createRenderer( ) function is called automatically.
We have overriden this method so that is returns an instance of our QQuickFrameBufferObject.Renderer(QMLFBORenderer).

## Compatibility

The code was tested in PyCharm with the following combination:
- Python 3.9.7 + PySide2 5.15.2.1 + VTK 9.1.0 + PyVista 0.33.2 + Numpy 1.21.2

## Example

![Pyvista_Bar](output/Pyvista_Bar.gif)

![Pyvista_Globe](output/Pyvista_Globe.gif)
