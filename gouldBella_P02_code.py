import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance
import random


def get_maya_main_win():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class Copy_To_Curve():
    curve_name = "curve1"
    mesh_name = "pCone1"
    will_instance = False
    copy_num = 3
    use_copy_num = False
    spacing = 15.0
    is_spacing_random = False
    rotation = "Fixed"
    user_x = 90.0
    user_y = 90.0
    user_z = 80.0

    # now we need to figure out the rotation.

    def copy_to_curve(self):
        if self.use_copy_num is False:
            self.copy_num = self._calculate_copy_num()
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
            if self.rotation == "Unchanged":
                pass
            else:
                self.rotate_copy()

    def duplicate_to_curve(self):
        for duplicate in range(1, int(self.copy_num)+1):
            new_mesh = cmds.duplicate(self.mesh_name)[0]
            pos = self.get_curve_point(duplicate)
            cmds.select(new_mesh)
            cmds.move(pos[0], pos[1], pos[2])
            if self.rotation == "Unchanged":
                pass
            else:
                self.rotate_copy()

    def rotate_copy(self):
        if self.rotation == "Fixed":
            rotate_vector = [self.user_x, self.user_y, self.user_z]
        else:
            x = float(random.randrange(0, 361))
            y = float(random.randrange(0, 361))
            z = float(random.randrange(0, 361))
            rotate_vector = [x, y, z]
        cmds.rotate(rotate_vector[0], rotate_vector[1], rotate_vector[2])

    def calculate_curve_divider(self):
        curve_divider = 1.0/(float(self.copy_num)+1.0)
        return curve_divider

    def get_curve_point(self, copy):
        if self.is_spacing_random is False:
            curve_divider = self.calculate_curve_divider()
        else:
            curve_divider = random.random()
            copy = 1
        point_location = cmds.pointOnCurve(self.curve_name,
                                           parameter=(curve_divider*copy),
                                           position=True,
                                           turnOnPercentage=True)
        return point_location

    def get_point_rotation(self, copy):
        curve_divider = self.calculate_curve_divider()
        point_rotation = cmds.pointOnCurve(self.curve_name,
                                           parameter=(curve_divider*copy),
                                           tangent=True,
                                           turnOnPercentage=True)
        return point_rotation

    def freeze_transforms(self, new_mesh):
        cmds.makeIdentity(new_mesh, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)

    def _calculate_copy_num(self):
        curve_length = cmds.arclen(self.curve_name)
        copy_num = curve_length//self.spacing
        return copy_num


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

        self.rotate_layout = QtWidgets.QHBoxLayout()
        self.rotate_lbl = QtWidgets.QLabel("Rotation settings:")
        self.rotate_layout.addWidget(self.rotate_lbl)
        self.rotate_cmbx = QtWidgets.QComboBox()
        self.rotate_cmbx.addItem("Unchanged")
        self.rotate_cmbx.addItem("Fixed")
        self.rotate_cmbx.addItem("Random")
        self.rotate_layout.addWidget(self.rotate_cmbx)

        self.rotate_input_layout = QtWidgets.QHBoxLayout()
        self.x_lbl = QtWidgets.QLabel("X")
        self.x_dspnbx = QtWidgets.QDoubleSpinBox()
        self.y_lbl = QtWidgets.QLabel("Y")
        self.y_dspnbx = QtWidgets.QDoubleSpinBox()
        self.z_lbl = QtWidgets.QLabel("Z")
        self.z_dspnbx = QtWidgets.QDoubleSpinBox()
        self.x_dspnbx.setEnabled(False)
        self.y_dspnbx.setEnabled(False)
        self.z_dspnbx.setEnabled(False)
        self.rotate_input_layout.addWidget(self.x_lbl)
        self.rotate_input_layout.addWidget(self.x_dspnbx)
        self.rotate_input_layout.addWidget(self.y_lbl)
        self.rotate_input_layout.addWidget(self.y_dspnbx)
        self.rotate_input_layout.addWidget(self.z_lbl)
        self.rotate_input_layout.addWidget(self.z_dspnbx)

        self.copy_num_layout = QtWidgets.QHBoxLayout()
        self.copy_num_chkbx = QtWidgets.QCheckBox("# of copies:")
        self.copy_num_layout.addWidget(self.copy_num_chkbx)
        self.copy_num_spnbx = QtWidgets.QSpinBox()
        self.copy_num_spnbx.setMinimum(1)
        self.copy_num_spnbx.setEnabled(False)
        self.copy_num_layout.addWidget(self.copy_num_spnbx)
        self.spacing_rndm_chkbx = QtWidgets.QCheckBox("Random Spacing?")
        self.spacing_rndm_chkbx.setEnabled(False)

        self.spacing_layout = QtWidgets.QHBoxLayout()
        self.spacing_chkbx = QtWidgets.QCheckBox("Copy spacing:")
        self.spacing_layout.addWidget(self.spacing_chkbx)
        self.spacing_dspnbx = QtWidgets.QDoubleSpinBox()
        self.spacing_dspnbx.setMinimum(0.0)
        self.spacing_dspnbx.setDecimals(3)
        self.spacing_dspnbx.setEnabled(False)
        self.spacing_layout.addWidget(self.spacing_dspnbx)
        # ^ add random spacing option! Combobox for options, rndm function for random spacing

        self.copy_btn = QtWidgets.QPushButton("Copy to curve")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def _layout_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.mesh_layout)
        self.main_layout.addLayout(self.curve_layout)
        self.main_layout.addLayout(self.dup_inst_layout)
        self.main_layout.addLayout(self.rotate_layout)
        self.main_layout.addLayout(self.rotate_input_layout)
        self.main_layout.addLayout(self.copy_num_layout)
        self.main_layout.addWidget(self.spacing_rndm_chkbx)
        self.main_layout.addLayout(self.spacing_layout)
        self.main_layout.addWidget(self.copy_btn)
        self.main_layout.addWidget(self.cancel_btn)
        self.setLayout(self.main_layout)

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.copy_btn.clicked.connect(self.copy_to_curve)
        self.copy_num_chkbx.stateChanged.connect(self._on_copy_checked)
        self.spacing_chkbx.stateChanged.connect(self._on_spacing_checked)
        self.rotate_cmbx.currentIndexChanged.connect(self._rotate_cmbx_changed)

    def _rotate_cmbx_changed(self):
        if self.rotate_cmbx.currentIndex() == 1:
            self.x_dspnbx.setEnabled(True)
            self.y_dspnbx.setEnabled(True)
            self.z_dspnbx.setEnabled(True)
        else:
            self.x_dspnbx.setEnabled(False)
            self.y_dspnbx.setEnabled(False)
            self.z_dspnbx.setEnabled(False)

    def _on_copy_checked(self):
        if self.copy_num_chkbx.isChecked():
            self.copy_num_spnbx.setEnabled(True)
            self.spacing_chkbx.setChecked(False)
            self.spacing_rndm_chkbx.setEnabled(True)
        else:
            self.copy_num_spnbx.setEnabled(False)

    def _on_spacing_checked(self):
        if self.spacing_chkbx.isChecked():
            self.spacing_dspnbx.setEnabled(True)
            self.spacing_rndm_chkbx.setEnabled(False)
            self.copy_num_chkbx.setChecked(False)
            self.spacing_rndm_chkbx.setChecked(False)
        else:
            self.spacing_dspnbx.setEnabled(False)

    def _duplicate_or_instance(self):
        text = self.dup_inst_cmbx.currentIndex()
        if text == 0:
            return False
        else:
            return True

    def copy_to_curve(self):
        self.copy.mesh_name = self.mesh_input.text()
        self.copy.curve_name = self.curve_input.text()
        self.copy.will_instance = self._duplicate_or_instance()
        self.copy.copy_num = self.copy_num_spnbx.value()
        self.copy.rotation = self.rotate_cmbx.currentText()
        self.copy.use_copy_num = self.copy_num_chkbx.isChecked()
        self.copy.spacing = self.spacing_dspnbx.value()
        self.copy.is_spacing_random = self.spacing_rndm_chkbx.isChecked()
        self.copy.user_x = self.x_dspnbx.value()
        self.copy.user_y = self.y_dspnbx.value()
        self.copy.user_z = self.z_dspnbx.value()
        self.copy.copy_to_curve()


# notes from class 4/20/2026:
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
# thank you Professor Lim!!!!!!!###

# import gouldBella_P02_code as project2
# import importlib
# importlib.reload(project2)

# copy = project2.Copy_To_Curve()
# copy.copy_to_curve(curve_name="curve1", mesh_name="pSphere1")

# win = project2.Copy_Win()
# win.show()
