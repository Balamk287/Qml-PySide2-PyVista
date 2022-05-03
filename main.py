from __future__ import annotations
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickWindow

from source import QmlFbo
import sys

if __name__ == "__main__":
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']
    app = QApplication(sys_argv)
    qmlRegisterType(QmlFbo, "QmlFbo", 1, 0, "QmlFbo")
    engine = QQmlApplicationEngine()
    engine.load("main.qml")

    if not engine.rootObjects():
        print("ERROR in loading")
        sys.exit(-1)

    mainWin: QQuickWindow = engine.rootObjects()[0]
    mainWin.show()
    sys.exit(app.exec_())