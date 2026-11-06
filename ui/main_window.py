main_template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>761</width>
    <height>703</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>0</width>
    <height>0</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>Lynk - Мои подписки</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <property name="leftMargin">
     <number>30</number>
    </property>
    <property name="topMargin">
     <number>30</number>
    </property>
    <property name="rightMargin">
     <number>30</number>
    </property>
    <property name="bottomMargin">
     <number>30</number>
    </property>
    <item>
     <widget class="QLabel" name="headerLabel">
      <property name="font">
       <font>
        <pointsize>22</pointsize>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Ваши подписки</string>
      </property>
      <property name="alignment">
       <set>Qt::AlignmentFlag::AlignCenter</set>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QTableWidget" name="tableWidget">
      <property name="font">
       <font>
        <pointsize>8</pointsize>
       </font>
      </property>
      <property name="editTriggers">
       <set>QAbstractItemView::EditTrigger::NoEditTriggers</set>
      </property>
      <property name="dragEnabled">
       <bool>false</bool>
      </property>
      <property name="alternatingRowColors">
       <bool>false</bool>
      </property>
      <property name="selectionBehavior">
       <enum>QAbstractItemView::SelectionBehavior::SelectRows</enum>
      </property>
      <property name="showGrid">
       <bool>false</bool>
      </property>
      <column>
       <property name="text">
        <string>Название</string>
       </property>
      </column>
      <column>
       <property name="text">
        <string>Дата окончания</string>
       </property>
      </column>
      <column>
       <property name="text">
        <string>Стоимость</string>
       </property>
      </column>
      <column>
       <property name="text">
        <string>Категория</string>
       </property>
      </column>
     </widget>
    </item>
    <item>
     <layout class="QHBoxLayout" name="bottomLayout">
      <item>
       <widget class="QPushButton" name="btnAdd">
        <property name="minimumSize">
         <size>
          <width>220</width>
          <height>55</height>
         </size>
        </property>
        <property name="font">
         <font>
          <pointsize>16</pointsize>
          <bold>true</bold>
         </font>
        </property>
        <property name="text">
         <string>ДОБАВИТЬ</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>
    <item>
     <widget class="QPushButton" name="btnDelete">
      <property name="minimumSize">
       <size>
        <width>220</width>
        <height>55</height>
       </size>
      </property>
      <property name="font">
       <font>
        <pointsize>16</pointsize>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Удалить</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="btnTheme">
      <property name="enabled">
       <bool>true</bool>
      </property>
      <property name="sizePolicy">
       <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
        <horstretch>0</horstretch>
        <verstretch>0</verstretch>
       </sizepolicy>
      </property>
      <property name="minimumSize">
       <size>
        <width>100</width>
        <height>55</height>
       </size>
      </property>
      <property name="maximumSize">
       <size>
        <width>100</width>
        <height>55</height>
       </size>
      </property>
      <property name="font">
       <font>
        <pointsize>16</pointsize>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Тема</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

"""