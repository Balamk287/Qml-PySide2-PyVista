from __future__ import annotations
import numpy as np
import pyvista as pv
from PySide2.QtQuick import QQuickFramebufferObject
from PySide2.QtCore import QPoint,Slot,Qt,QEvent,QPointF,Signal
from PySide2.QtGui import QMouseEvent, QWheelEvent,QKeyEvent
from pyvista import PolyData,examples

import source

class QMLPlotter():
    def __init__(self):
        #3D Pyvista Bar
        dx, pts = 2, 10j
        N = 100
        R = np.random.random((N, 3)) * 2 * dx - dx
        V = np.exp(-((R ** 2).sum(axis=1)))

        # create the grid to Interpolate on
        X, Y, Z = np.mgrid[-dx:dx:pts, -dx:dx:pts, -dx:dx:pts]
        points = np.column_stack((Z, Y, X))

        self.data_set: PolyData = pv.wrap(points)
        self.plotter = pv.Plotter()
        self.sargs = dict(interactive=False, title_font_size=2, height=0.05, width=0.90, shadow=True, position_x=0.05,
                          position_y=0.01)
        self.actor = self.plotter.add_mesh(self.data_set, show_scalar_bar=True, scalar_bar_args=self.sargs, flip_scalars=False,
                              point_size=5.0, render_points_as_spheres=True, cmap="Reds", reset_camera=True,
                              render=False, smooth_shading=True,name="mymesh")
        self.plotter.view_isometric()


        #Pyvista globe
        """mesh = examples.download_topo_global()
        mesh.compute_normals(inplace=True)
        warp = mesh.warp_by_scalar(factor=0.5e-5)
        self.plotter = pv.Plotter()
        self.actor = self.plotter.add_mesh(warp,show_scalar_bar=False)"""


    def get(self):
        return self.plotter

class QmlFbo(QQuickFramebufferObject):

    sigToggle = Signal()
    sigMousePress = Signal(float, float, int, int, int)
    sigMouseReleased = Signal(float, float, int, int, int)
    sigMouseMove = Signal(float, float, int, int, int)
    sigMouseWheel = Signal(QPoint, int, int, int, QPoint, float, float)
    sigKeyPress = Signal(int, int, str)
    sigKeyRelease = Signal(int, int, str)

    def __init__(self) -> None:
        super().__init__()
        self.x = QMLPlotter()
        self.plotter = self.x.get()

        self.lastMouseButtonEvent: QMouseEvent = None
        self.lastMouseMoveEvent: QMouseEvent = None
        self.lastWheelEvent: QWheelEvent = None
        self.lastKeyEvent: QKeyEvent = None

        self.setAcceptedMouseButtons(Qt.AllButtons)
        self.setMirrorVertically(True)
        self.toggeled = True

        self.sigToggle.connect(self.toggle)
        self.sigMousePress.connect(self.onMousePressed)
        self.sigMouseReleased.connect(self.onMouseReleased)
        self.sigMouseMove.connect(self.onMouseMove)
        self.sigMouseWheel.connect(self.onMouseWheel)
        self.sigKeyPress.connect(self.onKeyPressed)
        self.sigKeyRelease.connect(self.onKeyReleased)

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        self.__renderer_obj = source.QmlFBORenderer(renderer=self.plotter.renderer)
        return self.__renderer_obj

    @Slot(float, float, int, int, int)
    def onMousePressed(
            self, x: float, y: float, button: int, buttons: int, modifiers: int
    ):
        #print("mouse press")
        self.lastMouseButtonEvent = QMouseEvent(QEvent.MouseButtonPress,
            QPointF(x, y),
            Qt.MouseButton(button),
            Qt.MouseButtons(buttons),
            Qt.KeyboardModifiers(modifiers),
        )
        self.lastMouseButtonEvent.ignore()
        self.update()

    @Slot(float, float, int, int, int)
    def onMouseReleased(
            self, x: float, y: float, button: int, buttons: int, modifiers: int
    ):
        #print("mouse release")
        self.lastMouseButtonEvent = QMouseEvent(QEvent.MouseButtonRelease,
            QPointF(x, y),
            Qt.MouseButton(button),
            Qt.MouseButtons(buttons),
            Qt.KeyboardModifiers(modifiers),
        )
        self.lastMouseButtonEvent.ignore()
        self.update()

    @Slot(float, float, int, int, int)
    def onMouseMove(
            self, x: float, y: float, button: int, buttons: int, modifiers: int
    ):
        #print("mouse move")
        self.lastMouseMoveEvent = QMouseEvent(QEvent.MouseMove,
                                              QPointF(x, y),Qt.MouseButton(button),
                                              Qt.MouseButtons(buttons),Qt.KeyboardModifiers(modifiers))
        self.lastMouseMoveEvent.ignore()
        self.update()

    @Slot(QPoint, int, int, int, QPoint, float, float)
    def onMouseWheel(
            self,
            angleDelta: QPoint,
            buttons: int,
            inverted: int,
            modifiers: int,
            pixelDelta: QPoint,
            x: float,
            y: float,
    ):
        #print("mouse wheel")
        self.lastWheelEvent = QWheelEvent(
            QPointF(x, y),
            QPointF(x, y),
            pixelDelta,
            angleDelta,
            Qt.MouseButtons(buttons),
            Qt.KeyboardModifiers(modifiers),
            Qt.NoScrollPhase,
            bool(inverted),
        )
        self.lastWheelEvent.ignore()
        self.update()


    @Slot(int,int,str)
    def onKeyPressed(self,key:int,modifiers:int,text:str):

        self.lastKeyEvent = QKeyEvent(QEvent.KeyPress,Qt.Key(key),Qt.KeyboardModifiers(modifiers),text)

        if text == 'v':
            self.plotter.view_isometric()

        if text == 'b':
            self.plotter.show_bounds(xlabel='xRange[m]', ylabel='yRange[m]', zlabel='', grid='outer', location='outer',
                                     all_edges=True, minor_ticks=True, ticks='both')

        if text == 'q':
            self.window().close()

        self.lastKeyEvent.ignore()
        self.update()

    @Slot(int, int, str)
    def onKeyReleased(self, key: int, modifiers: int, text: str):
        self.lastKeyEvent = QKeyEvent(QEvent.KeyRelease,Qt.Key(key),Qt.KeyboardModifiers(modifiers),text)
        self.lastKeyEvent.ignore()
        self.update()

    @Slot()
    def toggle(self):
        self.toggeled = not self.toggeled
        if not self.toggeled:
            self.plotter.remove_actor(self.x.actor)
            self.update()
        else:
            self.plotter.add_actor(self.x.actor)
            self.update()