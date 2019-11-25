"""
                            spectralUI
--------------------------------------------------------------------
    Author: Tom George Ampiath
    Github: https://github.com/TomAmpiath
--------------------------------------------------------------------
"""

from PyQt5.QtWidgets import QApplication,\
    QMainWindow, QWidget, QFileDialog, QAction,\
    QSplitter, QHBoxLayout, QVBoxLayout,\
    QTableWidget, QTableWidgetItem, QGroupBox,\
    QHeaderView, QLabel, QPushButton,\
    QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIntValidator,\
    QIcon

from os import path
import sys

from scipy.io import loadmat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,\
    NavigationToolbar2QT
from matplotlib.figure import Figure
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('spectralUI')
        self.setMinimumSize(800, 600)
        self.showFullScreen()

        # ---------------Menubar----------------

        self.main_menu = self.menuBar()
        self.main_menu.setNativeMenuBar(False)

        self.file_menu = self.main_menu.addMenu("File")
        self.settings_menu = self.main_menu.addMenu("Settings")
        self.help_menu = self.main_menu.addMenu("Help")

        self.open_action = QAction("Open", self)
        self.exit_action = QAction("Exit", self)
        self.settings_action = QAction("Settings", self)
        self.help_action = QAction("Help", self)
        self.about_action = QAction("About", self)

        self.open_action.setShortcut("Ctrl+O")
        self.exit_action.setShortcut("Ctrl+Q")
        self.settings_action.setShortcut("Ctrl+P")
        self.help_action.setShortcut("Ctrl+H")
        self.about_action.setShortcut("Ctrl+A")

        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.exit_action)
        self.settings_menu.addAction(self.settings_action)
        self.help_menu.addAction(self.help_action)
        self.help_menu.addAction(self.about_action)

        self.open_action.triggered.connect(self.open_file)
        self.exit_action.triggered.connect(self.close)

        # -------------------Main Layout-----------------

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        self.main_nav_toolbar = NavigationToolbar2QT(
            self.main_canvas,
            self.main_widget
        )
        self.axes = self.main_canvas.figure.add_subplot()

        self.meta_data = QTableWidget()
        self.meta_data.setRowCount(9)
        self.meta_data.setColumnCount(2)
        self.meta_data.setEditTriggers(QTableWidget.NoEditTriggers)
        self.meta_data.setHorizontalHeaderItem(0, QTableWidgetItem("Property"))
        self.meta_data.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))
        self.meta_data.setAlternatingRowColors(True)
        self.meta_data.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.meta_data.setItem(0, 0, QTableWidgetItem("Filename"))
        self.meta_data.setItem(1, 0, QTableWidgetItem("File Size"))
        self.meta_data.setItem(2, 0, QTableWidgetItem("Data"))
        self.meta_data.setItem(3, 0, QTableWidgetItem("Height"))
        self.meta_data.setItem(4, 0, QTableWidgetItem("Width"))
        self.meta_data.setItem(5, 0, QTableWidgetItem("No: of Bands"))
        self.meta_data.setItem(6, 0, QTableWidgetItem(
            "Max. Intensity of Current Band"))
        self.meta_data.setItem(7, 0, QTableWidgetItem(
            "Min. Intensity of Current Band"))
        self.meta_data.setItem(8, 0, QTableWidgetItem(
            "Avg. Intensity of Current Band"))

        self.spectral_signature_canvas = FigureCanvasQTAgg(
            Figure(figsize=(5, 3))
        )
        self.spectral_axes = self.spectral_signature_canvas.figure.\
            add_subplot()
        self.spectral_nav_toolbar = NavigationToolbar2QT(
            self.spectral_signature_canvas,
            self.main_widget
        )

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout_sub = QVBoxLayout()
        self.vbox_layout_spectral = QVBoxLayout()
        self.hbox_layout_sub = QHBoxLayout()
        self.hbox_layout_sub_sub = QHBoxLayout()

        self.label = QLabel("Choose Band ->")
        self.band_text = QLineEdit()
        self.button = QPushButton("Load Band")

        self.band_text.setEnabled(False)
        self.button.setEnabled(False)

        self.int_validator = QIntValidator()
        self.band_text.setValidator(self.int_validator)
        self.band_text.returnPressed.connect(self.load_new_band)
        self.button.clicked.connect(self.load_new_band)

        self.hbox_layout_sub_sub.addWidget(self.label)
        self.hbox_layout_sub_sub.addWidget(self.band_text)
        self.hbox_layout_sub_sub.addWidget(self.button)

        self.hbox_layout_sub.addWidget(self.main_nav_toolbar)
        self.hbox_layout_sub.addLayout(self.hbox_layout_sub_sub)

        self.vbox_layout_sub.addWidget(self.main_canvas)
        self.vbox_layout_sub.addLayout(self.hbox_layout_sub)

        self.vbox_layout_spectral.addWidget(self.spectral_signature_canvas)
        self.vbox_layout_spectral.addWidget(self.spectral_nav_toolbar)

        self.main_group_box = QGroupBox("Image Analysis Tool")
        self.main_group_box.setMinimumSize(400, 300)
        self.main_group_box.setLayout(self.vbox_layout_sub)

        self.meta_box_layout = QHBoxLayout()
        self.meta_box_layout.addWidget(self.meta_data)

        self.meta_group_box = QGroupBox("Metadata")
        self.meta_group_box.setLayout(self.meta_box_layout)

        self.spectral_group_box = QGroupBox("Spectral Signature")
        self.main_group_box.setMinimumSize(350, 300)
        self.spectral_group_box.setLayout(self.vbox_layout_spectral)

        self.splitter_top_horizontal = QSplitter(Qt.Horizontal)
        self.splitter_vertical = QSplitter(Qt.Vertical)

        self.splitter_top_horizontal.addWidget(
            self.main_group_box
        )
        self.splitter_top_horizontal.addWidget(
            self.meta_group_box
        )
        self.splitter_top_horizontal.setSizes([200, 200])

        self.splitter_vertical.addWidget(self.splitter_top_horizontal)
        self.splitter_vertical.addWidget(self.spectral_group_box)
        self.splitter_vertical.setSizes([200, 200])

        self.vbox_layout.addWidget(self.splitter_vertical)

        self.centralWidget().setLayout(self.vbox_layout)

    def load_new_band(self):
        b = self.band_text.text()
        if len(b) < 1:
            alert = QMessageBox()
            alert.setText('Please enter a band value!') 
            alert.exec_()
        elif 0 <= int(b) < self.datacube.shape[2]:
            self.update_meta_data(
                self.filename, self.var_name, self.datacube, int(b)
            )
            self.update_canvas(self.datacube, int(b))
        else:
            alert = QMessageBox()
            alert.setText(
                'Please enter a value b/w 0 and '+
                str(self.datacube.shape[2])+'!'
                ) 
            alert.exec_()

    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(
            None,
            "Select Image",
            "",
            "Image File (*.mat)"
        )
        if self.filename:
            self.mat_file = loadmat(self.filename)
            self.var_name = list(self.mat_file.keys())[3]
            self.datacube = loadmat(
                self.filename,
                variable_names=self.var_name,
                appendmat=True).get(self.var_name)
            self.band_text.setEnabled(True)
            self.button.setEnabled(True)
            self.update_meta_data(
                self.filename, self.var_name, self.datacube, 0
            )
            self.update_canvas(self.datacube, 0)

    def file_size_estimate(self, file_size):
        for x in ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']:
            if file_size < 1024.0:
                return f'{file_size:.1f} {x}'
            file_size /= 1024.0

    def update_meta_data(self, file, var_name, image, band):
        self.meta_data.setItem(0, 1, QTableWidgetItem(path.basename(file)))
        self.meta_data.setItem(1, 1, QTableWidgetItem(
            str(self.file_size_estimate(path.getsize(file)))
            )
        )
        self.meta_data.setItem(2, 1, QTableWidgetItem(var_name))
        self.meta_data.setItem(3, 1, QTableWidgetItem(
            str(image.shape[0])
            )
        )
        self.meta_data.setItem(4, 1, QTableWidgetItem(
            str(image.shape[1])
            )
        )
        self.meta_data.setItem(5, 1, QTableWidgetItem(
            str(image.shape[2])
            )
        )
        self.meta_data.setItem(6, 1, QTableWidgetItem(
            str(np.amax(image[:, :, band]))
            )
        )
        self.meta_data.setItem(7, 1, QTableWidgetItem(
            str(np.amin(image[:, :, band]))
            )
        )
        self.meta_data.setItem(8, 1, QTableWidgetItem(
            str(np.mean(image[:, :, band]))
            )
        )
        self.meta_data.repaint()

    def plot_spectral_signature(self, event):
        self.x_coordinate = int(event.xdata)
        self.y_coordinate = int(event.ydata)
        self.spectral_axes.clear()
        self.spectral_axes.set_xlim(0, self.datacube.shape[2])
        self.spectral_axes.plot(
            [self.datacube[self.y_coordinate,
                           self.x_coordinate,
                           bnd] for bnd in range(0, self.datacube.shape[2])]
        )
        self.spectral_signature_canvas.draw_idle()

    def update_canvas(self, plot_input, band):
        self.axes.clear()
        self.axes.imshow(plot_input[:, :, band])
        self.main_canvas.draw_idle()
        self.main_canvas.repaint()
        self.main_canvas.mpl_connect(
            "button_press_event",
            self.plot_spectral_signature
        )


def set_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle("Fusion")
    
    icon_path = path.join(path.dirname(sys.modules[__name__].__file__), 'icon.png')
    app.setWindowIcon(QIcon(icon_path))

    dark_mode = False
    if dark_mode is True:
        app.setPalette(set_dark_palette())
        app.setStyleSheet(
            "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
            )

    main_window = MainWindow()

    exit_code = app.exec()
    sys.exit(exit_code)
