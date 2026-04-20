import MASH.api as mapi
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


class Duplicate_To_Curve():
    curve = "curve1"
    mesh = "pSphere1"
    instance = False

class Duplicate_To_Curve_Window():

# def create_mash_network():
# mashNetwork = mapi.Network()
# mashNetwork.createNetwork(name="duplicate_to_curve")
# node = mashNetwork.addNode("MASH_curve")
# cmds.setAttr(mashNetwork.distribute + ".arrangement", 4)
# cmds.connectAttr(mesh.outMesh, mashNetwork.distribute + ".inputMesh" )

### notes from class 4/20/2026: 
# look at Maya docs curve commands for inspo.
# Maya API is a plugin, so possible but not optimal.
# Return to this^ solution if you can't figure out anything else.
# pointOnCurve - returns info for a point on a curve
# can be used to find points halfway through (or other fractions) through curve
# pointOnCurve -pr 0.5 -p curve1;
# ^returns the xyz of a point halfway thru the curve.
# start of curve is 0, end of curve is 1.
# use turnOnPercentage=True to make sure positioning works.
# can also query the length of a curve if needed.
# arcLengthDimension or arclen
# reminder: for cmds.move, you cant just put entire [x, y, z] in there
# you have to separate it out with commas, like
# pos = [x, y, z]
# cmds.move(pos[0], pos[1], pos[2])
# also, the maya docs have both mel and python versions?? Check top right corner??
# thank you Professor Lim!!!!!!!###
