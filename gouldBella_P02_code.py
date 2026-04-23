import MASH.api as mapi
import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance


def get_maya_main_win():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class Duplicate_To_Curve():
    curve = "curve1"
    mesh = "pSphere1"
    instance = False
    duplicate_num = 3

    def duplicate_to_curve(self):
        for duplicate in range(1, self.duplicate_num+1):
            pos = self.get_curve_point(duplicate)
            cmds.select(duplicate)
            cmds.move(pos[0], pos[1], pos[2])

    def calculate_curve_divider(self):
        curve_divider = 1.0/(self.duplicate_num+1)
        return curve_divider

    def get_curve_point(self, duplicate):
        curve_divider = self.calculate_curve_divider()
        point_location = cmds.pointOnCurve(self.curve,
                                           parameter=(curve_divider*duplicate),
                                           position=True)
        return point_location


class Duplicate_Win(QtWidgets.QDialog):

    def __init__(self):
        super(Duplicate_Win, self).__init__(parent=get_maya_main_win())
        self.duplicate = Duplicate_To_Curve()
        self.setWindowTitle("Duplicate to Curve")
        self.resize(500, 500)
        self._define_widgets()
        self._layout_ui()
        self._connect_signals()

    def _define_widgets():
        pass

    def _layout_ui():
        pass

    def _connect_signals():
        pass



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
