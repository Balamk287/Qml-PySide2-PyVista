import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Window 2.3
import QtQuick.Controls.Material 2.12
import QmlFbo 1.0

ApplicationWindow {
    id: root
    width: 1024
    height: 800
    visible: true
    title: "Qml-PySide2-PyVista"

    Material.primary: Material.Indigo
    Material.accent: Material.LightBlue

    Rectangle {
        id: screenCanvasUI
        objectName: "canvasRect"
        anchors.fill: parent

        signal test_button;

        QmlFbo {
            id: fbo
            objectName: "fbo"
            anchors.fill: parent
            focus:true

            Keys.onPressed:
            {
                event.accepted = true;
                fbo.sigKeyPress(event.key,event.modifiers,event.text);
            }

            Keys.onReleased:
            {
                event.accepted = true;
                fbo.sigKeyRelease(event.key,event.modifiers,event.text);
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.AllButtons
                propagateComposedEvents: false

                onPressed: (mouse) => {
                    mouse.accepted = true;
                    fbo.sigMousePress(mouse.x, mouse.y, mouse.button,mouse.buttons, mouse.modifiers);
                }

                onReleased: (mouse) => {
                    mouse.accepted = true;
                    fbo.sigMouseReleased(mouse.x, mouse.y, mouse.button,mouse.buttons, mouse.modifiers);
                }

                onPositionChanged: (mouse) => {
                    fbo.sigMouseMove(mouse.x, mouse.y, mouse.button,mouse.buttons, mouse.modifiers);
                }

                onWheel: (wheel) => {
                    fbo.sigMouseWheel(wheel.angleDelta, wheel.buttons,wheel.inverted, wheel.modifiers,wheel.pixelDelta, wheel.x, wheel.y);
                }
            }

        }

        Button
        {
            id:btn
            text: "Show/Hide"
            highlighted: true
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 50
            onClicked: {
                fbo.sigToggle();
            }

            onActiveFocusChanged: {
                fbo.forceActiveFocus()
            }

        }
    }
}