import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance


def get_maya_main_win():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class Copy_To_Curve():
    curve = "curve1"
    mesh = "pSphere1"
    instance = False
    copy_num = 3

    def pick_duplicate_or_instance(self):
        if self.instance is True:
            self.instance_to_curve()
        else:
            self.duplicate_to_curve()

    def instance_to_curve(self):
        for instance in range(1, self.copy_num+1):
            new_mesh = cmds.instance(self.mesh)[0]
            pos = self.get_curve_point(instance)
            cmds.select(new_mesh)
            cmds.move(pos[0], pos[1], pos[2])
            self.freeze_transforms(new_mesh)
        
    def duplicate_to_curve(self):
        for duplicate in range(1, self.copy_num+1):
            new_mesh = cmds.duplicate(self.mesh)[0]
            pos = self.get_curve_point(duplicate)
            cmds.select(new_mesh)
            cmds.move(pos[0], pos[1], pos[2])

    def calculate_curve_divider(self):
        curve_divider = 1.0/(self.copy_num+1)
        return curve_divider

    def get_curve_point(self, duplicate):
        curve_divider = self.calculate_curve_divider()
        point_location = cmds.pointOnCurve(self.curve,
                                           parameter=(curve_divider*duplicate),
                                           position=True)
        return point_location
    
    def freeze_transforms(self, new_mesh):
        cmds.makeIdentity(new_mesh, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)


class Copy_Win(QtWidgets.QDialog):

    def __init__(self):
        super(Copy_Win, self).__init__(parent=get_maya_main_win())
        self.copy = Copy_To_Curve()
        self.setWindowTitle("Copy to Curve")
        self.resize(500, 500)
        self._define_widgets()
        self._layout_ui()
        self._connect_signals()

    def _define_widgets():
        # self.mesh_layout = QtWidgets.QHBoxLayout()
        # mesh label and input box
        # curve layout, label, input box
        # duplicate or instance layout, label and dropdown
        # number of copies layout, label, spin box
        # copy button
        # cancel button
        pass

    def _layout_ui():
        # self.main_layout = QtWidgets.QVBoxLayout()
        # self.main_layout.addLayout(x all layouts)
        # self.main_layout.addWidget(x all widgets)
        pass

    def _connect_signals():
        # self.cancel_btn.clicked.connect(self.close)
        # self.copy_btn.clicked.connect(self.copy_to_curve)
        # connect all other values with their widgets
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
