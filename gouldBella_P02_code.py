import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance


def get_maya_main_win():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)

# def class duplicate_to_curve():
# this will be the object that takes the mesh and duplicates it
# along the specified curve.

# so maybe I could use a MASH network?

# curve = curve1
# mesh = pSphere1

# select(-r "pSphere1")
# cmds.MASHnewNetwork("MASH#")
# setAttr("MASH1_Distribute.amplitudeX"=0)

# possible helpful documentation
# sweep mesh creator node: https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=GUID-28464AF4-6CB8-498A-93CB-ED70F971B478
# sweep mesh options: https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=GUID-515863CF-D31E-4D70-ADAB-0E36F342EB37
# custom sweep mesh: https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=GUID-BEECAB77-5F83-4BCF-9E6D-10EAC13514A8
