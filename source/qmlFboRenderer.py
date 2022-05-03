from __future__ import annotations
from PySide2.QtQuick import QQuickFramebufferObject
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QMouseEvent, QWheelEvent,QKeyEvent,QCursor
from PySide2.QtCore import Qt,QEvent
from vtkmodules.vtkRenderingExternal import vtkExternalOpenGLRenderWindow
import vtk
import source

Key = Qt.Key

_keysyms_for_ascii = (
    None, None, None, None, None, None, None, None,
    None, "Tab", None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    "space", "exclam", "quotedbl", "numbersign",
    "dollar", "percent", "ampersand", "quoteright",
    "parenleft", "parenright", "asterisk", "plus",
    "comma", "minus", "period", "slash",
    "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "colon", "semicolon", "less", "equal", "greater", "question",
    "at", "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z", "bracketleft",
    "backslash", "bracketright", "asciicircum", "underscore",
    "quoteleft", "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t", "u", "v", "w",
    "x", "y", "z", "braceleft", "bar", "braceright", "asciitilde", "Delete",
    )

_keysyms = {
    Key.Key_Backspace: 'BackSpace',
    Key.Key_Tab: 'Tab',
    Key.Key_Backtab: 'Tab',
    # Key.Key_Clear : 'Clear',
    Key.Key_Return: 'Return',
    Key.Key_Enter: 'Return',
    Key.Key_Shift: 'Shift_L',
    Key.Key_Control: 'Control_L',
    Key.Key_Alt: 'Alt_L',
    Key.Key_Pause: 'Pause',
    Key.Key_CapsLock: 'Caps_Lock',
    Key.Key_Escape: 'Escape',
    Key.Key_Space: 'space',
    # Key.Key_Prior : 'Prior',
    # Key.Key_Next : 'Next',
    Key.Key_End: 'End',
    Key.Key_Home: 'Home',
    Key.Key_Left: 'Left',
    Key.Key_Up: 'Up',
    Key.Key_Right: 'Right',
    Key.Key_Down: 'Down',
    Key.Key_SysReq: 'Snapshot',
    Key.Key_Insert: 'Insert',
    Key.Key_Delete: 'Delete',
    Key.Key_Help: 'Help',
    Key.Key_0: '0',
    Key.Key_1: '1',
    Key.Key_2: '2',
    Key.Key_3: '3',
    Key.Key_4: '4',
    Key.Key_5: '5',
    Key.Key_6: '6',
    Key.Key_7: '7',
    Key.Key_8: '8',
    Key.Key_9: '9',
    Key.Key_A: 'a',
    Key.Key_B: 'b',
    Key.Key_C: 'c',
    Key.Key_D: 'd',
    Key.Key_E: 'e',
    Key.Key_F: 'f',
    Key.Key_G: 'g',
    Key.Key_H: 'h',
    Key.Key_I: 'i',
    Key.Key_J: 'j',
    Key.Key_K: 'k',
    Key.Key_L: 'l',
    Key.Key_M: 'm',
    Key.Key_N: 'n',
    Key.Key_O: 'o',
    Key.Key_P: 'p',
    Key.Key_Q: 'q',
    Key.Key_R: 'r',
    Key.Key_S: 's',
    Key.Key_T: 't',
    Key.Key_U: 'u',
    Key.Key_V: 'v',
    Key.Key_W: 'w',
    Key.Key_X: 'x',
    Key.Key_Y: 'y',
    Key.Key_Z: 'z',
    Key.Key_Asterisk: 'asterisk',
    Key.Key_Plus: 'plus',
    Key.Key_Minus: 'minus',
    Key.Key_Period: 'period',
    Key.Key_Slash: 'slash',
    Key.Key_F1: 'F1',
    Key.Key_F2: 'F2',
    Key.Key_F3: 'F3',
    Key.Key_F4: 'F4',
    Key.Key_F5: 'F5',
    Key.Key_F6: 'F6',
    Key.Key_F7: 'F7',
    Key.Key_F8: 'F8',
    Key.Key_F9: 'F9',
    Key.Key_F10: 'F10',
    Key.Key_F11: 'F11',
    Key.Key_F12: 'F12',
    Key.Key_F13: 'F13',
    Key.Key_F14: 'F14',
    Key.Key_F15: 'F15',
    Key.Key_F16: 'F16',
    Key.Key_F17: 'F17',
    Key.Key_F18: 'F18',
    Key.Key_F19: 'F19',
    Key.Key_F20: 'F20',
    Key.Key_F21: 'F21',
    Key.Key_F22: 'F22',
    Key.Key_F23: 'F23',
    Key.Key_F24: 'F24',
    Key.Key_NumLock: 'Num_Lock',
    Key.Key_ScrollLock: 'Scroll_Lock',
    }

class QmlFBORenderer(QQuickFramebufferObject.Renderer):

    def __init__(self, renderer) -> None:
        super().__init__()
        self.renderer = renderer
        self.renderer.GradientBackgroundOn()
        self.rw: vtkExternalOpenGLRenderWindow = vtkExternalOpenGLRenderWindow()
        self.rw.AddRenderer(self.renderer)
        self.rwi = vtk.vtkGenericRenderWindowInteractor()
        self.interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.rwi.SetInteractorStyle(self.interactor_style)
        self.rwi.SetRenderWindow(self.rw)

        self.__fbo: source.QmlFbo = None

        self.__lastMouseButtonEvent: QMouseEvent = None
        self.__lastMouseMoveEvent: QMouseEvent = None
        self.__lastWheelEvent: QWheelEvent = None
        self.__lastKeyEvent: QKeyEvent = None

        self.__saveX = 0
        self.__saveY = 0
        self.__saveModifiers = Qt.KeyboardModifier.NoModifier
        self.__saveButtons = Qt.MouseButton.NoButton


    def synchronize(self, item: QQuickFramebufferObject):
        if not self.__fbo:
            self.__fbo = item

        (w, h) = self.rw.GetSize()
        if int(self.__fbo.width()) != w or int(self.__fbo.height()) != h:
            self.rw.SetSize(int(self.__fbo.width()), int(self.__fbo.height()))

        if (
                self.__fbo.lastMouseButtonEvent
                and not self.__fbo.lastMouseButtonEvent.isAccepted()
        ):
            self.__lastMouseButtonEvent = self.cloneMouseEvent(
                self.__fbo.lastMouseButtonEvent
            )
            self.__lastMouseButtonEvent.ignore()
            self.__fbo.lastMouseButtonEvent.accept()
        if (
                self.__fbo.lastMouseMoveEvent
                and not self.__fbo.lastMouseMoveEvent.isAccepted()
            ):
            self.__lastMouseMoveEvent = self.cloneMouseEvent(self.__fbo.lastMouseMoveEvent)
            self.__lastMouseMoveEvent.ignore()
            self.__fbo.lastMouseMoveEvent.accept()

        if self.__fbo.lastWheelEvent and not self.__fbo.lastWheelEvent.isAccepted():
            self.__lastWheelEvent = self.cloneWheelEvent(self.__fbo.lastWheelEvent)
            self.__lastWheelEvent.ignore()
            self.__fbo.lastWheelEvent.accept()

        if self.__fbo.lastKeyEvent and not self.__fbo.lastKeyEvent.isAccepted():
            self.__lastKeyEvent = self.cloneKeyEvent(self.__fbo.lastKeyEvent)
            self.__lastKeyEvent.ignore()
            self.__fbo.lastKeyEvent.accept()


    def render(self):
        self.rw.Render()
        self.rwi.Start()

        if self.__lastMouseButtonEvent and not self.__lastMouseButtonEvent.isAccepted():
            self.__processMouseButtonEvent(self.__lastMouseButtonEvent)
            self.__lastMouseButtonEvent.accept()

        if self.__lastMouseMoveEvent and not self.__lastMouseMoveEvent.isAccepted():
            self.__processMouseMoveEvent(self.__lastMouseMoveEvent)
            self.__lastMouseMoveEvent.accept()

        if self.__lastWheelEvent and not self.__lastWheelEvent.isAccepted():
            self.__processWheelEvent(self.__lastWheelEvent)
            self.__lastWheelEvent.accept()

        if self.__lastKeyEvent and not self.__lastKeyEvent.isAccepted():
            self.keyPressReleaseEvent(self.__lastKeyEvent)
            self.__lastKeyEvent.accept()

        self.__fbo.window().resetOpenGLState()

    def __processMouseButtonEvent(self, event: QMouseEvent):
        ctrl, shift = self.__getCtrlShift(event)
        repeat = 0
        if event.type() == QEvent.MouseButtonDblClick:
            repeat = 1

        self.__setEventInformation(
            event.x(), event.y(), ctrl, shift, chr(0), repeat, None
        )
        if (
                event.type() == QEvent.MouseButtonPress
                or event.type() == QEvent.MouseButtonDblClick
        ):
            if event.button() == Qt.LeftButton:
                self.rwi.LeftButtonPressEvent()

            elif event.button() == Qt.RightButton:
                self.rwi.RightButtonPressEvent()
            elif event.button() == Qt.MidButton:
                self.rwi.MiddleButtonPressEvent()

        elif event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.rwi.LeftButtonReleaseEvent()
            elif event.button() == Qt.RightButton:
                self.rwi.RightButtonReleaseEvent()
            elif event.button() == Qt.MidButton:
                self.rwi.MiddleButtonReleaseEvent()

    def __processMouseMoveEvent(self, event: QMouseEvent):
        ctrl, shift = self.__getCtrlShift(event)

        self.__saveModifiers = event.modifiers()
        self.__saveButtons = event.buttons()
        self.__saveX = event.x()
        self.__saveY = event.y()
        self.__setEventInformation(event.x(), event.y(), ctrl, shift, chr(0), 0, None)
        self.rwi.MouseMoveEvent()

    def __processWheelEvent(self, event: QWheelEvent):
        ctrl, shift = self.__getCtrlShift(event)
        self.__setEventInformation(event.x(), event.y(), ctrl, shift, chr(0), 0, None)

        delta = event.delta()
        if delta > 0:
            self.rwi.MouseWheelForwardEvent()
        elif delta < 0:
            self.rwi.MouseWheelBackwardEvent()

    def __setEventInformation(self, x, y, ctrl, shift, key, repeat=0, keysum=None):
        scale = self.__getPixelRatio()
        if self.__fbo.mirrorVertically():
            (w, h) = self.rw.GetSize()
            y = h - y

        self.rwi.SetEventInformation(
            int(round(x * scale)),
            int(round(y * scale)),
            ctrl,
            shift,
            key,
            repeat,
            keysum,
        )

    def __getCtrlShift(self, event):
        ctrl = shift = False
        if hasattr(event, "modifiers"):
            if event.modifiers() & Qt.ShiftModifier:
                shift = True
            if event.modifiers() & Qt.ControlModifier:
                ctrl = True
        else:
            if self.__saveModifiers & Qt.ShiftModifier:
                shift = True
            if self.__saveModifiers & Qt.ControlModifier:
                ctrl = True
        return ctrl, shift

    def __getPixelRatio(self):
        pos = QCursor.pos()
        for screen in QApplication.screens():
            rect = screen.geometry()
            if rect.contains(pos):
                return screen.devicePixelRatio()
        return QApplication.instance().devicePixelRatio()

    def keyPressReleaseEvent(self, ev):

        key, keySym = self._GetKeyCharAndKeySym(ev)
        ctrl, shift = self.__getCtrlShift(ev)
        self.__setEventInformation(self.__saveX,self.__saveY, ctrl, shift,key, 0,keySym)
        if ev.type() == QEvent.KeyPress:
            #print("key press")
            self.rwi.KeyPressEvent()
            self.rwi.CharEvent()
        if ev.type() == QEvent.KeyRelease:
            #print("key release")
            self.rwi.KeyReleaseEvent()

    def _GetKeyCharAndKeySym(self, ev):
        try:
            keyChar = ev.text()[0]
            keySym = _keysyms_for_ascii[ord(keyChar)]
        except IndexError:
            keyChar = '\0'
            keySym = None

        # next, try converting Qt key code to a VTK keysym
        if keySym is None:
            try:
                keySym = _keysyms[ev.key()]
            except KeyError:
                keySym = None

        # use "None" as a fallback
        if keySym is None:
            keySym = "None"
        return keyChar, keySym

    def cloneMouseEvent(self,event: QMouseEvent):
        return QMouseEvent(
            event.type(),
            event.localPos(),
            event.windowPos(),
            event.screenPos(),
            event.button(),
            event.buttons(),
            event.modifiers(),
            event.source(),
        )

    def cloneWheelEvent(self,event: QWheelEvent):
        return QWheelEvent(
            event.posF(),
            event.globalPosF(),
            event.pixelDelta(),
            event.angleDelta(),
            event.buttons(),
            event.modifiers(),
            event.phase(),
            event.inverted(),
            event.source(),
        )

    def cloneKeyEvent(self,event: QKeyEvent):
        return QKeyEvent(
            event.type(),
            event.key(),
            event.modifiers(),
            event.nativeScanCode(),
            event.nativeVirtualKey(),
            event.nativeModifiers(),
            event.text(),
        )
