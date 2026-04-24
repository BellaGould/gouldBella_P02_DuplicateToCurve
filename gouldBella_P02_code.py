import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance


def get_maya_main_win():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class Copy_To_Curve():
    curve_name = "curve1"
    mesh_name = "pSphere1"
    will_instance = False
    copy_num = 3

    def copy_to_curve(self):
        if self.will_instance is True:
            self.instance_to_curve()
        else:
            self.duplicate_to_curve()

    def instance_to_curve(self):
        for instance in range(1, self.copy_num+1):
            new_mesh = cmds.instance(self.mesh_name)[0]
            pos = self.get_curve_point(instance)
            cmds.select(new_mesh)
            cmds.move(pos[0], pos[1], pos[2])
            self.freeze_transforms(new_mesh)
        
    def duplicate_to_curve(self):
        for duplicate in range(1, self.copy_num+1):
            new_mesh = cmds.duplicate(self.mesh_name)[0]
            pos = self.get_curve_point(duplicate)
            cmds.select(new_mesh)
            cmds.move(pos[0], pos[1], pos[2])

    def calculate_curve_divider(self):
        curve_divider = 1.0/(self.copy_num+1)
        return curve_divider

    def get_curve_point(self, duplicate):
        curve_divider = self.calculate_curve_divider()
        point_location = cmds.pointOnCurve(self.curve_name,
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

    def _define_widgets(self):
        self.mesh_layout = QtWidgets.QHBoxLayout()
        self.mesh_lbl = QtWidgets.QLabel("Mesh name:")
        self.mesh_layout.addWidget(self.mesh_lbl)
        self.mesh_input = QtWidgets.QLineEdit()
        self.mesh_input.setPlaceholderText("pSphere1")
        self.mesh_layout.addWidget(self.mesh_input)

        self.curve_layout = QtWidgets.QHBoxLayout()
        self.curve_lbl = QtWidgets.QLabel("Curve name:")
        self.curve_layout.addWidget(self.curve_lbl)
        self.curve_input = QtWidgets.QLineEdit()
        self.curve_input.setPlaceholderText("curve1")
        self.curve_layout.addWidget(self.curve_input)

        self.dup_inst_layout = QtWidgets.QHBoxLayout()
        self.dup_inst_lbl = QtWidgets.QLabel("Duplicate or instance?")
        self.dup_inst_layout.addWidget(self.dup_inst_lbl)
        self.dup_inst_cmbx = QtWidgets.QComboBox()
        self.dup_inst_cmbx.addItem("Duplicate")
        self.dup_inst_cmbx.addItem("Instance")
        self.dup_inst_layout.addWidget(self.dup_inst_cmbx)

        self.copy_num_layout = QtWidgets.QHBoxLayout()
        self.copy_num_lbl = QtWidgets.QLabel("# of copies:")
        self.copy_num_layout.addWidget(self.copy_num_lbl)
        self.copy_num_spnbx = QtWidgets.QSpinBox()
        self.copy_num_spnbx.setMinimum(1)
        self.copy_num_layout.addWidget(self.copy_num_spnbx)
        
        self.copy_btn = QtWidgets.QPushButton("Copy to curve")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def _layout_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.mesh_layout)
        self.main_layout.addLayout(self.curve_layout)
        self.main_layout.addLayout(self.dup_inst_layout)
        self.main_layout.addLayout(self.copy_num_layout)
        self.main_layout.addWidget(self.copy_btn)
        self.main_layout.addWidget(self.cancel_btn)

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.copy_btn.clicked.connect(self.copy_to_curve)
        # connect all other values with their widgets

    def _duplicate_or_instance(self):
        text = self.dup_inst_cmbx.currentText()
        if text == "Duplicate":
            return False
        else:
            return True

    def copy_to_curve(self):
        self.copy.mesh_name = self.mesh_input.text()
        self.copy.curve_name = self.curve_input.text()
        self.copy.will_instance = self._duplicate_or_instance()
        self.copy.copy_num = self.copy_num_spnbx.value()
        self.copy.copy_to_curve()



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
