#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import reg
#import richtextlineedit

class GenericDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}
    def insertColumnDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate
    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QItemDelegate.paint(self, painter, option, index)
    def createEditor(self, parent, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QItemDelegate.createEditor(self, parent, option,index)
    def editorEvent(self, event, model, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.editorEvent( event, model, option, index)
        else:
            return QItemDelegate.editorEvent(self, event, model, option, index)
    def setEditorData(self, editor, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QItemDelegate.setEditorData(self, editor, index)
    def setModelData(self, editor, model, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QItemDelegate.setModelData(self, editor, model, index)
    def setDelegates(self, delegates):
        for index, delegate in enumerate(delegates):
            if delegate == "num":
                self.insertColumnDelegate(index, NumDelegate())
            elif delegate == "checkbox":
                self.insertColumnDelegate(index, CheckBoxDelegate())
            else:
                "raise error here"
                return 

class NumDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(NumDelegate,self).__init__(parent)
    def createEditor(self,parent,option,index):
        lineEdit= QLineEdit(parent)
        lineEdit.setFrame(False)
        regExp =reg.match_one_num
        validator = QRegExpValidator(regExp)
        lineEdit.setValidator(validator)
        return lineEdit
    def setEditorData(self,editor,index):
        value = index.model().data(index,Qt.UserRole)
        if editor is not None:
            editor.setText(value)
    def setModelData(self, editor, model,index):
        if not editor.isModified():
            return
        text = editor.text()
        validator = editor.validator()
        if validator is not None:
            state, text =validator.validate(text,0)

        if state == QValidator.Acceptable:
            color = '#ffffff' #white
            model.setData(index, editor.text())
class IntegerColumnDelegate(QItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum


    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return spinbox


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toInt()[0]
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))

class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CheckBoxDelegate, self).__init__(parent)
    def createEditor(self,parent,option, index):
        """important, other wise an editor is created if the user clicks in this cell."""
        return None
    def paint(self, painter, option, index):
        checked = index.data().toBool()
        check_box_style_option= QStyleOptionButton()

        if (index.flags() & Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly

        if checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)
        check_box_style_option.state |= QStyle.State_Enabled
        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)
    def editorEvent(self, event, model, option, index):
        if not (index.flags() & Qt.ItemIsEditable) > 0:
            return False
        if event.type() == QEvent.MouseButtonPress \
                or event.type() == QEvent.MouseMove:
            return False
        if event.type() == QEvent.MouseButtonRelease \
                or event.type() == QEvent.MouseButtonDblClick:
            if event.button() != Qt.LeftButton :
                return False
            if event.type() == QEvent.MouseButtonDblClick \
                    and event.button() is Qt.LeftButton:
                print "double click"
                return True # why are we returning true, how to we go to the bottom of the code?
        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space \
                    and event.key() != Qt.Key_Select:
                return False
            else:
                return False
        print event.type(), 'button',event.button()
        self.setModelData(None, model,index)
        return True
    def setModelData(self, editor, model, index):
        newValue = not(index.model().data(index, Qt.DisplayRole) == True)
        model.setData(index, newValue, Qt.EditRole)
    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect= QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(option.rect.x() +
                                option.rect.width() /2 -
                                check_box_rect.width() / 2,
                                option.rect.y() +
                                option.rect.height() /2 -
                                check_box_rect.height() /2)
        return QRect(check_box_point, check_box_rect.size())

class DateColumnDelegate(QItemDelegate):

    def __init__(self, minimum=QDate(), maximum=QDate.currentDate(),
                 format="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = QString(format)


    def createEditor(self, parent, option, index):
        dateedit = QDateEdit(parent)
        dateedit.setDateRange(self.minimum, self.maximum)
        dateedit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        dateedit.setDisplayFormat(self.format)
        dateedit.setCalendarPopup(True)
        return dateedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toDate()
        editor.setDate(value)
    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.date()))

class PlainTextColumnDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(PlainTextColumnDelegate, self).__init__(parent)
    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        return lineedit
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)
    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.text()))

class RichTextColumnDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(RichTextColumnDelegate, self).__init__(parent)
    def paint(self, painter, option, index):
        text = index.model().data(index, Qt.DisplayRole).toString()
        palette = QApplication.palette()
        document = QTextDocument()
        document.setDefaultFont(option.font)
        if option.state & QStyle.State_Selected:
            document.setHtml(QString("<font color=%1>%2</font>") \
                    .arg(palette.highlightedText().color().name()) \
                    .arg(text))
        else:
            document.setHtml(text)
        painter.save()
        color = palette.highlight().color() \
            if option.state & QStyle.State_Selected \
            else QColor(index.model().data(index,
                    Qt.BackgroundColorRole))
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)
        painter.restore()
    def sizeHint(self, option, index):
        text = index.model().data(index).toString()
        document = QTextDocument()
        document.setDefaultFont(option.font)
        document.setHtml(text)
        return QSize(document.idealWidth() + 5,
                     option.fontMetrics.height())
    def createEditor(self, parent, option, index):
        #lineedit = richtextlineedit.RichTextLineEdit(parent)
        lineedit
        return lineedit
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setHtml(value)
    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.toSimpleHtml()))
