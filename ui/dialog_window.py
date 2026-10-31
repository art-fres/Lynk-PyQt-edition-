dialog_template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>AddSubscriptionDialog</class>
 <widget class="QDialog" name="AddSubscriptionDialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>520</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Добавление подписки</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <property name="spacing">
    <number>12</number>
   </property>
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
    <widget class="QLabel" name="titleLabel">
     <property name="font">
      <font>
       <pointsize>14</pointsize>
       <bold>true</bold>
      </font>
     </property>
     <property name="text">
      <string>Введите название</string>
     </property>
     <property name="alignment">
      <set>Qt::AlignmentFlag::AlignCenter</set>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="labelName">
     <property name="font">
      <font>
       <pointsize>11</pointsize>
      </font>
     </property>
     <property name="text">
      <string>Название</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLineEdit" name="inputName">
     <property name="minimumSize">
      <size>
       <width>0</width>
       <height>40</height>
      </size>
     </property>
     <property name="placeholderText">
      <string>Введите название</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="labelDate">
     <property name="font">
      <font>
       <pointsize>11</pointsize>
      </font>
     </property>
     <property name="text">
      <string>Дата</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QDateEdit" name="inputDate">
     <property name="minimumSize">
      <size>
       <width>0</width>
       <height>40</height>
      </size>
     </property>
     <property name="displayFormat">
      <string>dd.MM.yyyy</string>
     </property>
     <property name="calendarPopup">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="labelCost">
     <property name="font">
      <font>
       <pointsize>11</pointsize>
      </font>
     </property>
     <property name="text">
      <string>Стоимость</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLineEdit" name="inputCost">
     <property name="minimumSize">
      <size>
       <width>0</width>
       <height>40</height>
      </size>
     </property>
     <property name="placeholderText">
      <string>Введите сумму</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="labelCategory">
     <property name="font">
      <font>
       <pointsize>11</pointsize>
      </font>
     </property>
     <property name="text">
      <string>Категория подписки</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QComboBox" name="comboCategory">
     <property name="minimumSize">
      <size>
       <width>0</width>
       <height>40</height>
      </size>
     </property>
    </widget>
   </item>
   <item>
    <spacer name="verticalSpacer">
     <property name="orientation">
      <enum>Qt::Orientation::Vertical</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>0</width>
       <height>0</height>
      </size>
     </property>
    </spacer>
   </item>
   <item>
    <layout class="QHBoxLayout" name="buttonLayout">
     <property name="spacing">
      <number>15</number>
     </property>
     <item>
      <widget class="QPushButton" name="btnSave">
       <property name="minimumSize">
        <size>
         <width>0</width>
         <height>45</height>
        </size>
       </property>
       <property name="text">
        <string>ДОБАВИТЬ</string>
       </property>
       <property name="default">
        <bool>true</bool>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="btnCancel">
       <property name="minimumSize">
        <size>
         <width>0</width>
         <height>45</height>
        </size>
       </property>
       <property name="text">
        <string>ОТМЕНА</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""