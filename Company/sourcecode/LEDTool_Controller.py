import sys
import os
import cv2
import re
from datetime import datetime
from dshow import get_camera_monikers
from CameraProperty import get_camera_property_range
from LEDDealer import Led_Selected, LED_SpecCalculate, Find_Average_Hue, Change_Selection_Length
from INI import write_ini, read_ini

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize, QTimer, QPoint, QEvent
from PySide6.QtGui import QIcon, QPixmap, QImage, QIntValidator, QBrush, QColor
from qtrangeslider import QRangeSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.photodir = os.path.join(self.current_directory,'TempPhoto')
        os.makedirs(self.photodir, exist_ok=True)
        
        self.slider_hovered = False  # 新增一個標記來跟踪滑塊是否被懸停
        self.select_length_changed = False
        self.cameraconfig = dict()
        self.user_config_path = str()
        self.user_pic_path = str()
        self.table_window = None
             
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("LED Config Setting Tool")
        #self.setGeometry(150, 150, 1000, 600)
        self.setFixedSize(1015, 550)
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(5, 5, 360, 530)

        self.Tab1_Set()
        self.Tab0_Set()
        self.Tab2_Set()

        self.statusBar().showMessage('Ready')  #這個要放在這

    #region 相機設置頁簽排版
    def Tab1_Set(self):
        self.tab1 = QWidget(self)     
        self.tab_widget.addTab(self.tab1, "相機設置")
        self.Tab1_1_Load_Camera()
        self.Tab1_2_Camera_Controls()
        self.Tab1_3_Load_Config()
        self.Tab1_TakePicture() 
    
    #region tab1_1
    def Tab1_1_Load_Camera(self):
        self.group_box1_1 = QGroupBox("Load Camera", self.tab1)
        self.group_box1_1.setGeometry(5, 5, 345, 110)
        group_Vlayout = QVBoxLayout(self.group_box1_1)

        H_layout = QHBoxLayout()
        self.Cameralist_Combo = QComboBox(self.tab1, objectName="Cameralist")
        self.Cameralist_Combo.setFixedHeight(20)
        self.Get_Camrealist()

        file_path = os.path.join(self.current_directory, 'icon', 'refresh.png')
        refresh_button = QPushButton(self.tab1)
        refresh_button.setIcon(QIcon(QPixmap(file_path)))
        refresh_button.setFixedSize(QSize(20, 20))
        refresh_button.setIconSize(refresh_button.size())  
        refresh_button.clicked.connect(self.Get_Camrealist)  

        H_layout.addWidget(self.Cameralist_Combo)
        H_layout.addWidget(refresh_button)

        H_layout2 = QHBoxLayout()
        self.connect_button = QPushButton("相機連接", self.tab1)
        self.connect_button.setFixedSize(QSize(120, 30))
        H_layout2.addWidget(self.connect_button)
        self.disconnect_button = QPushButton("相機關閉", self.tab1)
        self.disconnect_button.setFixedSize(QSize(120, 30))
        H_layout2.addWidget(self.disconnect_button)
        group_Vlayout.addLayout(H_layout)
        group_Vlayout.addLayout(H_layout2)

        self.disconnect_button.setEnabled(False)

        self.connect_button.clicked.connect(self.Open_Camera)
        self.disconnect_button.clicked.connect(self.Close_Camera)   
    #endregion tab1_1
       
    #region tab1_2
    def Tab1_2_Camera_Controls(self):
        self.group_box1_2 = QGroupBox("Camera Controls", self.tab1)
        self.group_box1_2.setGeometry(5, 115, 345, 220)
        group_Vlayout = QVBoxLayout(self.group_box1_2)
        self.group_box1_2.setEnabled(False)

        self.setting_name = ['Brightness', 'Contrast','Saturation', 'Exposure', 'Gain', 'WhiteBalance']
        name_ch = ['亮度', '對比', '飽和度', '曝光', '增益', '白平衡']
        
        for i, name in enumerate(self.setting_name):
            left_Hlayout1 = QHBoxLayout()
            camere_control_lebal = QLabel(name_ch[i], self.tab1)
            camere_control_slider = IntervalSlider(Qt.Orientation.Horizontal, self.tab1, objectName=f"slider_{name}")
            camere_control_slider.valueChanged.connect(self.ChangeSliderValue)
            #camere_control_slider.installEventFilter(self)  # 安裝事件過濾器
            camere_control_slider.setFixedWidth(220)
            camere_control_slider.setRange(0, 300)
            camere_control_line = QLineEdit(self.tab1, objectName=f"line_{name}")
            camere_control_line.editingFinished.connect(self.ChangeLineValue)
            camere_control_line.setFixedHeight(20)  # Set height
            camere_control_line.setFixedWidth(50)  # Set width
            camere_control_line.setText(str(camere_control_slider.value()))

            left_Hlayout1.addWidget(camere_control_lebal)
            left_Hlayout1.addWidget(camere_control_slider)
            left_Hlayout1.addWidget(camere_control_line)
            group_Vlayout.addLayout(left_Hlayout1)
    
    def ChangeSliderValue(self):
        sender = self.sender()
        Slider = self.tab1.findChild(QSlider, sender.objectName())
        slidername = Slider.objectName()
        name = slidername.split('_')[1]
        line = self.tab1.findChild(QLineEdit, f"line_{name}")
        line.setText(str(Slider.value()))
        print(f"{slidername}, {Slider.value()}")
        self.SetCameraPorperty(name, int(Slider.value()))
        self.show_value_tooltip(Slider, Slider.value())
        self.CameraConfig_change(name, Slider.value())
    
    def ChangeLineValue(self):
        sender = self.sender()
        Lineedit = self.tab1.findChild(QLineEdit, sender.objectName())
        Lineeditname = Lineedit.objectName()
        name = Lineeditname.split('_')[1]
        slider = self.tab1.findChild(QSlider, f"slider_{name}")
        slider.setValue(int(Lineedit.text()))
        self.SetCameraPorperty(name, int(Lineedit.text()))
        self.CameraConfig_change(name, Lineedit.text())

    def Set_PropertyValue(self, cameraproperty:dict):
        #cameraproperty ={'Brightness': (0, 255, 1, 128), 'Contrast': (0, 255, 1, 32), 'Saturation': (0, 255, 1, 32), 'Exposure': (-13, 0, 1, -6), 'Gain': (0, 255, 1, 0), 'WhiteBalance': (0, 10000, 10, 4000)}
        #value = (0, 255, 1, 128) min, max, step, default
        print(cameraproperty)
        for name, value in cameraproperty.items():
            slider = self.tab1.findChild(QSlider, f"slider_{name}")
            line = self.tab1.findChild(QLineEdit, f"line_{name}")
            slider.setEnabled(True)
            line.setEnabled(True)
            if type(value) == tuple:
                slider.setMinimum(int(value[0]))
                slider.setMaximum(int(value[1]))
                slider.setInterval(int(value[2]))          
                int_validator = QIntValidator(int(value[0]), int(value[1]), self)
                line.setValidator(int_validator)
                slider.setValue(int(value[3]))
            else:
                slider.setValue(int(value))
    #endregion tab1_2
    
    #region tab1_3
    def Tab1_3_Load_Config(self):
        self.group_box1_3 = QGroupBox("Load Config", self.tab1)
        self.group_box1_3.setGeometry(5, 335, 345, 100)
        group_Vlayout = QVBoxLayout(self.group_box1_3)
        self.group_box1_3.setEnabled(False)

        H_Layout = QHBoxLayout()
        self.loadconfig_button = QPushButton("載入設定檔", self.tab1)
        self.loadconfig_button.setFixedSize(QSize(80, 25))
        self.loadconfig_button.clicked.connect(self.loadcameraconfig)
        self.CameraConfig_Combo = QComboBox(self.tab1, objectName="CameraConfig")
        self.CameraConfig_Combo.setFixedHeight(23)
        H_Layout.addWidget(self.loadconfig_button)
        H_Layout.addWidget(self.CameraConfig_Combo)

        H_Layout2 = QHBoxLayout()
        self.saveconfig_button = QPushButton("儲存設定", self.tab1)
        self.saveconfig_button.setFixedSize(QSize(90, 25))
        self.saveconfig_button.setEnabled(False)
        self.saveconfig_button.clicked.connect(self.ConfigSave)
        H_Layout2.addStretch()
        H_Layout2.addWidget(self.saveconfig_button)

        group_Vlayout.addLayout(H_Layout)
        group_Vlayout.addLayout(H_Layout2)
    #endregion tab1_3

    def Tab1_TakePicture(self):
        self.photo_button = QPushButton("拍照", self.tab1)
        self.photo_button.resize(QSize(150, 50))
        self.photo_button.move(100, 445)
        self.photo_button.clicked.connect(self.TakePhoto)
        self.photo_button.setEnabled(False)
    #endregion 相機設置頁簽排版

    #region 相機畫面顯示頁簽排版
    def Tab0_Set(self):
        self.tab0_widget = QTabWidget(self)
        self.tab0_widget.setGeometry(370, 5, 640, 530)
        self.stream_label = QLabel(self)
        self.image_label = QLabel(self)
        self.stream_label.setFixedSize(self.tab0_widget.width(), self.tab0_widget.height())
        self.image_label.setFixedSize(self.tab0_widget.width(), self.tab0_widget.height())
        self.tab0_widget.addTab(self.stream_label, '相機串流')
        self.tab0_widget.addTab(self.image_label, '照片')
    #endregion 相機顯示頁簽排版

    #region 相機設置
    def Get_Camrealist(self):
        self.Cameralist_Combo.clear()
        self.Cameralist = get_camera_monikers()
        print(self.Cameralist)
        for camera in self.Cameralist:   
            ind, name, path, _ = camera
            self.Cameralist_Combo.addItem(name)
        self.Cameralist_Combo.setCurrentIndex(-1) 
        self.statusBar().showMessage('Refresh Done!')
    
    def Open_Camera(self):
        ind = self.Cameralist_Combo.currentIndex()
        if ind == -1:
            self.statusBar().showMessage('請先選擇相機!')
            return       
        cameraproperty = get_camera_property_range(self.Cameralist[ind][2]) #獲得該相機參數
        self.cap = cv2.VideoCapture(ind, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap.release()
            QMessageBox.warning(self, 'WARNING', '無法開啟相機!')
            return
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        self.Set_PropertyValue(cameraproperty)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.disconnect_button.setEnabled(True)
        self.group_box1_2.setEnabled(True)
        self.group_box1_3.setEnabled(True)
        self.photo_button.setEnabled(True)
    
    def update_frame(self):
        try:
            ret, self.frame = self.cap.read()
            if ret:
                frame_resized = cv2.resize(self.frame, (self.stream_label.width(), self.stream_label.height()))
                frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                q_img = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.stream_label.setPixmap(pixmap)
            else:
                self.Close_Camera()
                QMessageBox.warning(self, 'WARNING', '偵測到相機失去連接!')
        except Exception as ex:
            self.Close_Camera()
            QMessageBox.warning(self, 'WARNING', f'相機發生Exceptopn!\r\n{ex}')

    def SetCameraPorperty(self, property_name, value):     
        if property_name == 'WhiteBalance':
            if not self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE, value):
                if not self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, value):
                    if not self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, value):
                        self.Disable_Property(property_name)                
        else:
            cap_prop_name = f"CAP_PROP_{property_name.upper()}"
            cap_prop_value = getattr(cv2, cap_prop_name, None)
            if not self.cap.set(cap_prop_value, value):
                self.Disable_Property(property_name)
    
    def Disable_Property(self, property_name):
        slider = self.tab1.findChild(QSlider, f"slider_{property_name}")
        line = self.tab1.findChild(QLineEdit, f"line_{property_name}")
        slider.setEnabled(False)
        line.setEnabled(False)
        QMessageBox.warning(self, 'WARNING', f'相機{property_name}無法調整!')   
    
    def TakePhoto(self):
        now = datetime.now()
        formatted_time = now.strftime('%Y%m%d%H%M%S')
        self.photopath = os.path.join(self.photodir, f'{formatted_time}.jpg')
        cv2.imwrite(self.photopath, self.frame)
        self.displayImage(self.photopath)
        self.statusBar().showMessage(f'儲存成功! 路徑:{self.photopath}')
         
    def Close_Camera(self):
        self.timer.stop()
        self.cap.release()
        self.cap = None
        self.stream_label.clear()
        self.group_box1_2.setEnabled(False)
        self.CameraConfig_Combo.clear()
        self.photo_button.setEnabled(False)
        self.saveconfig_button.setEnabled(False)
        self.Cameralist_Combo.setCurrentIndex(-1)
        self.group_box1_3.setEnabled(False)

    def displayImage(self, img):
        if type(img) == str:
            img = cv2.imread(img)
            if img is None:
                self.statusBar().showMessage(f"Error: Could not load image from {img}")
                return
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        qImg = QImage(img_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(pixmap)
        self.tab0_widget.setCurrentIndex(1)
        self.tab0_widget.setFocus()
    #endregion 相機設置
    
    #region 相機config設置
    def loadcameraconfig(self):
        self.camconfigpath = self.open_cameraconfig_dialog()
        if self.camconfigpath:
            result = self.configcheck()
            if not result:
                return     
            self.CameraConfig_Combo_set()
            self.saveconfig_button.setEnabled(True)
            self.statusBar().showMessage('Camera config loaded successfully!')

    def open_cameraconfig_dialog(self):
        options = QFileDialog.Options()
        self.user_config_path, _ = QFileDialog.getOpenFileName(self, "Open Config File", self.user_config_path, 
                                                    "Images (*.ini *.text);;All Files (*)", 
                                                    options=options)
        return self.user_config_path
    
    def configcheck(self):
        self.cameraconfig = read_ini(self.camconfigpath)
        section_keys= ['Red','Green','Amber','Blue','Black','White','CameraPath']
        #print(self.cameraconfig)
        for section, options in self.cameraconfig.items():
            tmp_list = list()
            if not any(key.lower() in section.lower() for key in section_keys):
                QMessageBox.warning(self, "Config Check Error",f"Camera Config中，section名子必須包含{'、'.join(section_keys)}其中一個字串")
                return False
            for option, value in options.items():
                tmp_list.append(option)

            diff = set(self.setting_name) - set(tmp_list)
            if section != 'CameraPath' and len(diff):
                QMessageBox.warning(self, "Config Check Error",f"Camera Config中，section {section}中缺少{'、'.join(diff)}")
                return False
        return True   
    
    def CameraConfig_Combo_set(self):
        for section, options in self.cameraconfig.items():
            if section != 'CameraPath':
                self.CameraConfig_Combo.addItem(section)
        self.CameraConfig_Combo.setCurrentIndex(-1)
        self.CameraConfig_Combo.currentTextChanged.connect(self.CameraConfig_Combo_change)
    
    def CameraConfig_Combo_change(self):
        if self.CameraConfig_Combo.currentIndex() != -1:
            section_name = self.CameraConfig_Combo.currentText()
            setting = self.cameraconfig[section_name]
            for name, value in setting.items():
                self.SetCameraPorperty(name, int(value))
            self.Set_PropertyValue(setting)
    
    def CameraConfig_change(self, propertyname, propertyvaule):
        if self.cameraconfig or len(self.cameraconfig):
            self.cameraconfig[self.CameraConfig_Combo.currentText()][propertyname] = propertyvaule
    
    def ConfigSave(self):
        self.camerapath_change()
        write_ini(self.camconfigpath, self.cameraconfig)
        self.statusBar().showMessage(f'Camera Config 儲存成功! 路徑:{self.camconfigpath}')
    
    def camerapath_change(self):
        ind = self.Cameralist_Combo.currentIndex()
        camerapath = self.Cameralist[ind][2]
        match = re.search(r'\\\\\?\\(.*?)#{', camerapath)
        nowcamerapath = None
        if match:
            nowcamerapath = match.group(1).replace('#','\\').upper()
        if nowcamerapath:
            if nowcamerapath != self.cameraconfig['CameraPath']['Path']:
                ref = QMessageBox.information(self, '更變提醒', '偵測到目前使用相機的CameraPath與Config中不同，是否同步修改Config?', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Cancel)
                if ref == QMessageBox.StandardButton.Ok:
                    self.cameraconfig['CameraPath']['Path'] = nowcamerapath
    #endregion 相機config設置
    
    #region LED設定頁簽排版
    def Tab2_Set(self):
        self.tab2 = QWidget(self)
        self.tab_widget.addTab(self.tab2, "LED設置")
        self.Tab2_1_LoadPhoto()
        self.Tab2_2_LED_Select()
        self.Tab2_3_LED_Setting()
        self.Tab2_GenConfig()
    
    #region tab2_1
    def Tab2_1_LoadPhoto(self):
        self.group_box2_1 = QGroupBox("Load Photo", self.tab2)
        self.group_box2_1.setGeometry(5, 5, 345, 70)
        group_Hlayout = QHBoxLayout(self.group_box2_1)

        self.loadphoto_btn = QPushButton("載入圖片", self.tab2)
        self.loadphoto_btn.clicked.connect(self.loadphoto)
        self.loadphoto_btn.resize(QSize(120, 60))

        group_Hlayout.addWidget(self.loadphoto_btn)
        group_Hlayout.addSpacing(170)

    def loadphoto(self):
        self.photopath = self.open_image_dialog()
        if self.photopath:
            self.displayImage(self.photopath)
            self.Table_close()
            self.group_box2_2.setEnabled(True)
            self.select_length_changed = False
            self.reset_tab2_2_value()
          
    def open_image_dialog(self):
        options = QFileDialog.Options()
        self.user_pic_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", self.user_pic_path, 
                                                    "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", 
                                                    options=options)
        return self.user_pic_path
    #endregion tab2_1
    
    #region tab2_2
    def Tab2_2_LED_Select(self):
        self.group_box2_2 = QGroupBox("Led Select", self.tab2)
        self.group_box2_2.setGeometry(5, 75, 345, 110)
        self.group_box2_2.setEnabled(False)
        group_Vlayout = QVBoxLayout(self.group_box2_2)
        
        group_Vlayout.addLayout(self.Tab2_2_LedSelectBtn())
        group_Vlayout.addLayout(self.Tab2_2_LedSelectLength())
            
    def Tab2_2_LedSelectBtn(self):
        group_Hlayout = QHBoxLayout()
        self.selection_btn = QPushButton("框選", self.tab2)
        self.selection_btn.clicked.connect(self.Showledselectresult)
        group_Hlayout.addWidget(self.selection_btn)
        return group_Hlayout
        
    def Showledselectresult(self):
        self.ledimage, self.point_data, self.selectable_length = Led_Selected(self.photopath)
        self.displayImage(self.ledimage)
        self.Table_close()
        self.select_widget_enable(True)
        self.select_length_changed = False
        average_h = Find_Average_Hue(self.photopath)
        if average_h != None:
            self.hue_slider.setValue(average_h*2)
      
        self.length_slider.setMinimum(self.selectable_length[0])
        self.length_slider.setMaximum(self.selectable_length[1])
        self.length_slider.setValue(self.selectable_length[0])
        self.length_line.setText("")
        self.length_range_label.setText(f"{self.selectable_length[0]} ~ {self.selectable_length[1]}")
        
        self.length_slider.valueChanged.connect(self.update_length_slider)
        self.length_line.editingFinished.connect(self.update_length_line)
    
    def Tab2_2_LedSelectLength(self):
        self.select_Hlayout = QHBoxLayout()
        length_label = QLabel("框選大小(L)", self.tab2)
        self.length_slider = QSlider(Qt.Orientation.Horizontal, self.tab2, objectName='slider_length')
        self.length_slider.setFixedHeight(20)
        self.length_slider.setFixedWidth(165)
        
        self.length_line = QLineEdit(self.tab2, objectName=f"line_length")
        self.length_line.setFixedHeight(20)  # Set height
        self.length_line.setFixedWidth(40)  # Set width
        
        self.length_range_label = QLabel("__ ~ __", self.tab2)
        
        self.select_Hlayout.addWidget(length_label)
        self.select_Hlayout.addWidget(self.length_slider)
        self.select_Hlayout.addWidget(self.length_line)
        self.select_Hlayout.addWidget(self.length_range_label)
        
        self.select_widget_enable(False)
        
        return self.select_Hlayout

    def update_length_slider(self, value):
        self.length_line.setText(str(value))
        self.select_length_changed = True
        print("update_length_slider")
        self.displayImage(Change_Selection_Length(self.photopath, self.point_data, int(value)))
        
    def update_length_line(self):
        self.length_slider.setValue(int(self.length_line.text()))
        #self.displayImage(Change_Selection_Length(self.photopath, self.center_point, int(self.length_line.text())))
    
    def reset_tab2_2_value(self):
        try:
            self.length_slider.valueChanged.disconnect()
        except RuntimeError:
            pass  
        try:
            self.length_line.editingFinished.disconnect()
        except RuntimeError:
            pass 
        self.select_widget_enable(False)
        self.length_range_label.setText("__ ~ __")
        self.length_slider.setMinimum(0)
        self.length_slider.setMaximum(10)
        self.length_slider.setValue(0)
        self.length_line.setText("")
        self.hue_slider.setValue(0)
    
    def select_widget_enable(self, enable:bool):
        for i in range(self.select_Hlayout.count()):
            widget = self.select_Hlayout.itemAt(i).widget()
            if widget:
                widget.setEnabled(enable) 
    #endregion tab2_2
    
    #region tab2_3
    def Tab2_3_LED_Setting(self):
        self.group_box2_3 = QGroupBox("Led Property", self.tab2)
        self.group_box2_3.setGeometry(5, 185, 345, 220)
        group_Vlayout = QVBoxLayout(self.group_box2_3)

        group_Vlayout.addLayout(self.Tab2_3_HueSlider())
        group_Vlayout.addLayout(self.Tab2_3_HueRange())
        group_Vlayout.addLayout(self.Tab2_3_SaturationSlider())
        group_Vlayout.addLayout(self.Tab2_3_ValueSlider())
        group_Vlayout.addLayout(self.Tab2_3_PreviewBtn())
       
    def Tab2_3_HueSlider(self):
        group_Hlayout = QHBoxLayout()
        hue_label = QLabel("色相(H)", self.tab2)
        self.hue_slider = QSlider(Qt.Orientation.Horizontal, self.tab2, objectName='slider_color')
        self.hue_slider.setMinimum(0)
        self.hue_slider.setMaximum(360)
        self.hue_slider.setTickPosition(QSlider.TicksBelow)
        self.hue_slider.setTickInterval(60)
        angles = [0, 60, 120, 180, 240, 300, 360]
        #self.colorangle_label(angles)

        self.hue_slider.setFixedHeight(20)
        self.hue_slider.setFixedWidth(230)
        self.hue_line = QLineEdit(self.tab2, objectName=f"line_color")
        self.hue_line.setFixedHeight(20)  # Set height
        self.hue_line.setFixedWidth(40)  # Set width
        self.hue_line.setText('0')

        group_Hlayout.addWidget(hue_label)
        group_Hlayout.addWidget(self.hue_slider)
        group_Hlayout.addWidget(self.hue_line)
        
        self.hue_slider.valueChanged.connect(self.update_h_slider)
        self.hue_line.editingFinished.connect(self.update_h_line)

        return group_Hlayout

    def colorangle_label(self, angles):
        slider_width = self.hue_slider.width() - 22  # Estimate the boundary width
    
        for angle in angles:
            label = QLabel(str(angle), self.tab2)
            label.setFixedWidth(50)  # Set width
            position_percentage = angle / 360
            print(label.width())
            position_pixel = (slider_width * position_percentage) - (label.width() / 2)
            print(position_pixel)
            label.move(position_pixel + 38, self.hue_slider.height() + 35)  # Move label to the desired position under the slider
    
    def Tab2_3_HueRange(self):
        group_Hlayout = QHBoxLayout()
        huerange_label = QLabel("範圍(Range)", self.tab2)
        self.huerange_slider = QSlider(Qt.Orientation.Horizontal, self.tab2, objectName='slider_range')
        self.huerange_slider.setMinimum(0)
        self.huerange_slider.setMaximum(30)
        self.huerange_slider.setValue(30)
        self.huerange_slider.setTickPosition(QSlider.TicksBelow)
        self.huerange_slider.setTickInterval(10)
        
        self.huerange_slider.setFixedHeight(20)
        self.huerange_slider.setFixedWidth(120)
        
        symbol_label = QLabel("±", self.tab2)
        
        self.huerange_line = QLineEdit(self.tab2, objectName=f"line_range")
        self.huerange_line.setFixedHeight(20)  # Set height
        self.huerange_line.setFixedWidth(30)  # Set width
        self.huerange_line.setText('30')
        
        group_Hlayout.addWidget(huerange_label)
        group_Hlayout.addWidget(self.huerange_slider)
        group_Hlayout.addWidget(symbol_label)
        group_Hlayout.addWidget(self.huerange_line)
        group_Hlayout.addStretch(1)
        
        self.huerange_slider.valueChanged.connect(self.update_range_slider)
        self.huerange_line.editingFinished.connect(self.update_range_line)
        
        return group_Hlayout

    def Tab2_3_SaturationSlider(self):
        group_Hlayout = QHBoxLayout()
        saturation_label = QLabel("飽和度(S)", self.tab2)
        self.saturation_slider = QRangeSlider(Qt.Orientation.Horizontal, self.tab2)
        self.saturation_slider.setRange(0, 255)
        self.saturation_slider.setValue([80,255]) 
        
        self.saturation_line_lower = QLineEdit(self.tab2, objectName=f"line_saturation_lower")
        self.saturation_line_lower.setFixedHeight(20)  # Set height
        self.saturation_line_lower.setFixedWidth(30)  # Set width
        self.saturation_line_lower.setText('80')

        self.saturation_line_upper = QLineEdit(self.tab2, objectName=f"line_saturation_upper")
        self.saturation_line_upper.setFixedHeight(20)  # Set height
        self.saturation_line_upper.setFixedWidth(30)  # Set width
        self.saturation_line_upper.setText('255')
        t_label = QLabel("~", self.tab2)

        group_Hlayout.addWidget(saturation_label)
        group_Hlayout.addWidget(self.saturation_slider)
        group_Hlayout.addWidget(self.saturation_line_lower)
        group_Hlayout.addWidget(t_label)
        group_Hlayout.addWidget(self.saturation_line_upper)

        self.saturation_slider.valueChanged.connect(self.update_s_slider)
        self.saturation_line_lower.editingFinished.connect(self.update_s_line)
        self.saturation_line_upper.editingFinished.connect(self.update_s_line)
        return group_Hlayout

    def Tab2_3_ValueSlider(self):
        group_Hlayout = QHBoxLayout()
        value_label = QLabel("明度(V)   ", self.tab2)
        self.value_slider = QRangeSlider(Qt.Orientation.Horizontal, self.tab2)
        self.value_slider.setRange(0, 255)
        self.value_slider.setValue([80,255]) 
        
        self.value_line_lower = QLineEdit(self.tab2, objectName=f"line_value_lower")
        self.value_line_lower.setFixedHeight(20)  # Set height
        self.value_line_lower.setFixedWidth(30)  # Set width
        self.value_line_lower.setText('80')

        self.value_line_upper = QLineEdit(self.tab2, objectName=f"line_value_upper")
        self.value_line_upper.setFixedHeight(20)  # Set height
        self.value_line_upper.setFixedWidth(30)  # Set width
        self.value_line_upper.setText('255')
        t_label = QLabel("~", self.tab2)

        group_Hlayout.addWidget(value_label)
        group_Hlayout.addWidget(self.value_slider)
        group_Hlayout.addWidget(self.value_line_lower)    
        group_Hlayout.addWidget(t_label)
        group_Hlayout.addWidget(self.value_line_upper)

        self.value_slider.valueChanged.connect(self.update_v_slider)
        self.value_line_lower.editingFinished.connect(self.update_v_line)
        self.value_line_upper.editingFinished.connect(self.update_v_line)
        return group_Hlayout

    def update_h_slider(self, value):
        self.hue_line.setText(str(value))
        color = self.get_color(value)
        self.show_value_tooltip(self.hue_slider, color)

    def update_h_line(self):
        self.hue_slider.setValue(int(self.hue_line.text()))
    
    def update_range_slider(self, value):
        self.huerange_line.setText(str(value))
    
    def update_range_line(self):
        self.huerange_slider.setValue(int(self.huerange_line.text()))

    def update_s_slider(self, value):
        self.saturation_line_lower.setText(str(value[0]))
        self.saturation_line_upper.setText(str(value[1]))
    
    def update_s_line(self):
        value = [int(self.saturation_line_lower.text()), (int(self.saturation_line_upper.text()))]
        self.saturation_slider.setValue(value)
                 
    def update_v_slider(self, value):
        self.value_line_lower.setText(str(value[0]))
        self.value_line_upper.setText(str(value[1]))
    
    def update_v_line(self, value):
        value = [int(self.value_line_lower.text()), (int(self.value_line_upper.text()))]
        self.value_slider.setValue(value)
    
    def get_color(self, value):
        if 0 <= value <= 90:
            return 'Amber'
        if 90 <= value <= 150:
            return 'Green'
        if 150 <= value <= 270:
            return 'Blue'
        if 270 <= value <= 360:
            return 'Red'
    
    def Tab2_3_PreviewBtn(self):
        group_Hlayout = QHBoxLayout()
        self.preview_btn = QPushButton('預覽結果', self.tab2)
        self.preview_btn.clicked.connect(self.Showledresult)
        group_Hlayout.addStretch(2)
        group_Hlayout.addWidget(self.preview_btn)
        return group_Hlayout
    
    def Showledresult(self):
        led_h = self.hue_slider.value()
        self.led_color = self.get_color(led_h)

        led_range = self.huerange_slider.value()
        led_s = self.saturation_slider.value()
        led_v = self.value_slider.value()
        led_spec = [int(led_h), int(led_range), led_s, led_v]
        self.selection_change_data()
        print("point_data", self.point_data)
        self.config, led_result = LED_SpecCalculate(self.photopath, self.point_data, led_spec)

        print("config", self.config)
        print("led_result", led_result)
        self.table_window = TableWindow(led_result)
        self.table_window.show()
    
    def Table_close(self):
        if self.table_window:
            self.table_window.close()
             
    def selection_change_data(self):
        if self.select_length_changed:
            user_length = int(self.length_line.text())
            self.point_data = {name:((data[0][0], data[0][1]),(user_length, user_length)) for name, data in self.point_data.items()}
    #endregion tab2_3  
    
    def Tab2_GenConfig(self):
        self.config_button = QPushButton("產生Config", self.tab2)
        self.config_button.resize(QSize(150, 50))
        self.config_button.move(100, 445)
        self.config_button.clicked.connect(self.saveled)
        self.config_button.clicked.connect(self.writeFile)
        self.config_button.setEnabled(True)
    
    def writeFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", f"{self.led_color}.ini", "Configuration Files (*.ini);;All Files (*)", options=options)
        if file_name:
            write_ini(file_name, self.config)
            QMessageBox.information(self, "Success", f"Data saved to {file_name}!")
    
    def saveled(self):
        now = datetime.now()
        formatted_time = now.strftime('%Y%m%d%H%M%S')
        ledpath = os.path.join(self.photodir, f'{formatted_time}.jpg')
        cv2.imwrite(ledpath, self.ledimage) 
    #endregion LED設定頁簽排版

    #region 其他小工具
    def show_value_tooltip(self, slider, value):
        # if not self.slider_hovered:  # 只有當滑鼠懸停在滑塊上時才顯示工具提示
        #     return
        #Calculate the position of the slider handle
        slider_min = slider.minimum()
        slider_max = slider.maximum()
        slider_range = slider.width()
        handle_x = ((slider.value() - slider_min) / (slider_max - slider_min)) * slider_range
        
        tooltip_offset = QPoint(handle_x, -35)  # -20 to display the tooltip above the handle
        # Convert the handle's local position to global screen position
        pos = slider.mapToGlobal(slider.rect().topLeft() + tooltip_offset)
        QToolTip.showText(pos, str(value), slider)

    def eventFilter(self, obj, event):
        if obj == IntervalSlider:
            if event.type() == QEvent.Enter:  # 滑鼠進入滑塊
                self.slider_hovered = True
                return True
            elif event.type() == QEvent.Leave:  # 滑鼠離開滑塊
                self.slider_hovered = False
                QToolTip.hideText()  # 隱藏工具提示
                return True

        return super().eventFilter(obj, event)
    #endregion 其他小工具



class IntervalSlider(QSlider):

    def __init__(self, *args, **kargs):
        super(IntervalSlider, self).__init__( *args, **kargs)
        self._min = 0
        self._max = 99
        self.interval = 1

    def setValue(self, value):
        index = round((value - self._min) / self.interval)
        return super(IntervalSlider, self).setValue(index)

    def value(self):
        return self.index * self.interval + self._min

    @property
    def index(self):
        return super(IntervalSlider, self).value()

    def setIndex(self, index):
        return super(IntervalSlider, self).setValue(index)

    def setMinimum(self, value):
        self._min = value
        self._range_adjusted()

    def setMaximum(self, value):
        self._max = value
        self._range_adjusted()

    def setInterval(self, value):
        # To avoid division by zero
        if not value:
            raise ValueError('Interval of zero specified')
        self.interval = value
        self._range_adjusted()

    def _range_adjusted(self):
        number_of_steps = int((self._max - self._min) / self.interval)
        super(IntervalSlider, self).setMaximum(number_of_steps)

    def maximum(self):
        return self._max
    
    def minimum(self):
        return self._min
    
    def stepvalue(self):
        return self.interval

class TableWindow(QWidget):
    def __init__(self, data:list):
        super().__init__()
        self.data = data
        self.Main_UI()  
        self.insert_data()
    
    def Create_frozontable(self):
        self.frozen_table = QTableWidget(self)
        self.frozen_table.setColumnCount(1)
        self.frozen_table.setSelectionMode(QTableWidget.NoSelection)
        self.frozen_table.setFocusPolicy(Qt.NoFocus)
        self.frozen_table.horizontalHeader().hide()
        self.frozen_table.resizeColumnsToContents()
        self.frozen_table.horizontalHeader().setVisible(False)
        
    def Create_maintable(self):
        self.main_table = QTableWidget(self)
        init = ['', 'Avg_H', 'Avg_S', 'Avg_V', 'All Count', 'Total Light Count', 'Total Pass Count', 'Pass Count (Config)']
        self.main_table.setColumnCount(1)
        self.main_table.setRowCount(len(init))

        #self.table.setStyleSheet("QTableWidget::item { border: 1px solid black; }")
        
        for row in range(self.main_table.rowCount()):
            for col in range(self.main_table.columnCount()):
                item = QTableWidgetItem(init[row])
            
                if col == 0 and row != 0:
                    brush = QBrush(QColor(211, 211, 211)) 
                    brush.setStyle(Qt.SolidPattern)
                    item.setBackground(brush)
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                self.main_table.setItem(row, col, item)

        self.main_table.resizeColumnsToContents()
        self.main_table.horizontalHeader().setVisible(False)
    
    def sync_scroll(self):
        sender = self.sender()
        if sender == self.frozen_table.horizontalScrollBar():
            self.main_table.horizontalScrollBar().setValue(self.frozen_table.horizontalScrollBar().value())
        else:
            self.frozen_table.horizontalScrollBar().setValue(self.main_table.horizontalScrollBar().value())
        
    
    def Main_UI(self):
        self.setWindowTitle("Result")
        self.Create_frozontable()
        self.Create_maintable()
        
        self.resize(700, self.get_table_height() + 50)
        
        layout = QVBoxLayout()
        layout.addWidget(self.frozen_table)
        layout.addWidget(self.main_table)
    
        self.setLayout(layout)
        
        self.frozen_table.horizontalScrollBar().valueChanged.connect(self.sync_scroll)
        self.main_table.horizontalScrollBar().valueChanged.connect(self.sync_scroll)
    
    
    def insert_data(self):
        self.main_table.setColumnCount(len(self.data))
        for row in range(self.main_table.rowCount()):
            for col in range(1, self.main_table.columnCount()):
                item = QTableWidgetItem(str(self.data[col-1][row]))

                if row == 0:
                    brush = QBrush(QColor(211, 211, 211)) 
                    brush.setStyle(Qt.SolidPattern)
                    item.setBackground(brush)
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)                
                self.main_table.setItem(row, col, item) 
    
    def get_table_height(self):
        # Initialize with the header height
        height = self.main_table.horizontalHeader().height()
        for i in range(self.main_table.rowCount()):
            height += self.main_table.rowHeight(i)
        return height            
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())