main_template="""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
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
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Ваши подписки</string>
      </property>
      <property name="alignment">
       <set>Qt::AlignCenter</set>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QTableWidget" name="tableWidget">
      <property name="showGrid">
       <bool>false</bool>
      </property>
      <property name="alternatingRowColors">
       <bool>false</bool>
      </property>
      <property name="selectionBehavior">
       <enum>QAbstractItemView::SelectRows</enum>
      </property>
      <property name="editTriggers">
       <set>QAbstractItemView::NoEditTriggers</set>
      </property>
      <property name="verticalHeaderVisible">
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
       <spacer name="spacerLeft">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
       </spacer>
      </item>
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
          <weight>75</weight>
          <bold>true</bold>
         </font>
        </property>
        <property name="text">
         <string>ДОБАВИТЬ</string>
        </property>
       </widget>
      </item>
      <item>
       <spacer name="spacerRight">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
       </spacer>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>"""