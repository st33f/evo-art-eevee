from presets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import glob
import os
import sys

PRESETS_PATH = 'data/presets/'
MASTER_CONFIG_PATH = 'data/master_'

class Gui(QDialog):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)
        self.setWindowTitle("Evo Art Puppetmaster")
        self.resize(540, 340)

        self.master_config_dict = load_config(MASTER_CONFIG_PATH)
        self.presetName = self.master_config_dict['preset_path'].split(os.sep)[-1]

        self.mainLayout = QGridLayout()

        self.createTopLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0)

        self.createPresetChooser()
        self.mainLayout.addLayout(self.PresetChooser, 1, 0)

        self.createDictEditor(self.master_config_dict['preset_path'])
        self.mainLayout.addLayout(self.DictEditor, 3, 0)

        #self.createConfigEditor(self.master_config_dict['preset_path'])
        #self.mainLayout.addLayout(self.ConfigEditor, 3, 0)

        # Initialize tab screen
        #self.tabLayout = QGridLayout()
        #self.tabs = QTabWidget()
        #self.tab1 = QWidget()
        #self.tab2 = QWidget()
        #self.tabs.resize(300, 200)
        # Add tabs
        #self.tabs.addTab(self.tab1, "Preset")
        #self.tabs.addTab(self.tab2, "Genes")
        # Create first tab
        #self.tab1.layout = QVBoxLayout(self)
        # self.createDictEditor(self.master_config_dict['preset_path'])
        #self.tab1.layout.addWidget(self.DictEditor)
        #self.pushButton1 = QPushButton("PyQt5 button 1")
        #self.tab1.layout.addWidget(self.pushButton1)



        #self.mainLayout.addWidget(self.tabs, 3, 0)



        #self.initTabs()
        #self.mainLayout.addLayout(self.tabLayout, 2, 0)

        self.setLayout(self.mainLayout)


    def createTopLayout(self):

        self.topLayout = QHBoxLayout()
        self.styleLabel = QLabel("Here you can edit the preset config file.")
        self.topLayout.addWidget(self.styleLabel)


    def initTabs(self):

        # Initialize tab screen
        self.tabLayout = QGridLayout()
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)
        # Add tabs
        self.tabs.addTab(self.tab1, "Preset")
        self.tabs.addTab(self.tab2, "Genes")
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        #self.createDictEditor(self.master_config_dict['preset_path'])
        #self.tab1.layout.addWidget(self.DictEditor)
        #self.pushButton1 = QPushButton("PyQt5 button 1")
        #self.tab1.layout.addWidget(self.pushButton1)
        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        #self.pushButton2 = QPushButton("PyQt5 button 2")
        #self.tab2.layout.addWidget(self.pushButton2)
        self.tabLayout.addWidget(self.tabs)


    def createPresetChooser(self, masterConfigPath=MASTER_CONFIG_PATH):
        presets = glob.glob(PRESETS_PATH + '*')
        preset_names = [x.split(os.sep)[-1] for x in presets]
        print(preset_names)

        self.PresetChooser = QHBoxLayout()

        #self.master_config_dict = load_config(masterConfigPath)

        self.presetComboBox = QComboBox()
        self.presetComboBox.addItems(preset_names)
        index = self.presetComboBox.findText(self.presetName)

        if index >= 0:
            self.presetComboBox.setCurrentIndex(index)

        self.presetComboBox.activated.connect(self.updateMasterConfig)

        presetLabel = QLabel("&Active preset:")
        presetLabel.setBuddy(self.presetComboBox)

        self.saveBtn = QPushButton("Select")
        self.saveBtn.clicked.connect(lambda: self.saveDict(self.master_config_dict, masterConfigPath))

        self.PresetChooser.addWidget(presetLabel)
        self.PresetChooser.addWidget(self.presetComboBox)
        self.PresetChooser.addWidget(self.saveBtn)
        #print(preset_names)


    def updateMasterConfig(self, index):
        self.master_config_dict = load_config()
        self.presetName = self.presetComboBox.itemText(index)
        #self.master_config_dict['preset_path'].split(os.sep)[-2]
        self.master_config_dict['preset_path'] = PRESETS_PATH + self.presetName + '/'



    def createDictEditor(self, presetPath):
        widgets = {}
        self.DictEditor = QFormLayout()
        config_dict = load_config(presetPath)
        for key, value in config_dict.items():
            widgets[key] = widget = {}
            widget['lineedit'] = lineedit = QLineEdit(str(value))
            self.DictEditor.addRow(key, lineedit)

        self.saveBtn = QPushButton("Save config")
        self.saveBtn.clicked.connect(lambda: self.saveDict(config_dict, presetPath))
        self.DictEditor.addRow(self.saveBtn)
    """


    def createConfigEditor(self, presetPath):
        config_dict = load_config(presetPath)
        self.ConfigEditor = QGridLayout()

        self.ConfigEditor.addWidget(QLabel("Bass"), 1, 1)
        self.ConfigEditor.addWidget(QLabel("Synth"), 1, 2)
        self.ConfigEditor.addWidget(QLabel("High perc"), 1, 3)
        self.ConfigEditor.addWidget(QLabel("Low perc"), 1, 4)

        self.ConfigEditor.addWidget(QLabel("mutation rate"), 2, 0)
        self.mut1 = QLineEdit(str(config_dict["mut_rate"]["bass"]))
        #self.mut1..connect(self.updateLocalConfig())

        self.ConfigEditor.addWidget(self.mut1)

        self.saveBtn = QPushButton("Save config")
        self.saveBtn.clicked.connect(lambda: self.saveDict(config_dict, presetPath))
        self.ConfigEditor.addWidget(self.saveBtn)


    def updateLocalConfig(self):
        pass
    """

    def saveDict(self, configDict, configPath):

        if sys.platform == "win32":
            configPath = os.path.normpath(configPath)

        print(f"saving config file as {configPath}config.json")
        save_config(configPath, configDict)


    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)


app = QApplication(sys.argv)
gui = Gui()
gui.show()
sys.exit(app.exec_())