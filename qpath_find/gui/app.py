# coding: UTF-8
import sys

from PySide import QtGui, QtCore


class TableWindow(QtGui.QWidget):

    def __init__(self, _map, path):
        QtGui.QWidget.__init__(self)
        self._map = _map
        rowcnt, colcnt = self._map.shape
        self.tablewidget = QtGui.QTableWidget(rowcnt, colcnt)

        for row in xrange(0, rowcnt):
            self.tablewidget.setRowHeight(row, 30)
            for col in xrange(0, colcnt):
                self.tablewidget.setColumnWidth(col, 30)
                self.tablewidget.setItem(row, col, QtGui.QTableWidgetItem())
                if self._map[row, col]:
                    self.tablewidget.item(row, col).setBackground(QtGui.QColor(0, 0, 0))

        for i, e in enumerate(path):
            x, y = e
            if i == 0:
                color = (255, 0, 0)
            elif i == len(path) - 1:
                color = (0, 128, 0)
            else:
                color = (255, 255, 0)
            self.tablewidget.item(x, y).setBackground(QtGui.QColor(*color))

        # Header formatting
        font = QtGui.QFont()
        font.setFamily(u"DejaVu Sans")
        font.setPointSize(12)
        self.tablewidget.horizontalHeader().setFont(font)
        self.tablewidget.verticalHeader().setFont(font)

# Font used
        font = QtGui.QFont()
        font.setFamily(u"DejaVu Sans")
        font.setPointSize(20)
        self.tablewidget.setFont(font)

# Global Size
        self.resize(33*rowcnt, 33*colcnt + 10)

# Layout of the table
        layout = QtGui.QGridLayout()
        layout.addWidget(self.tablewidget, 0, 0)
        self.setLayout(layout)



def main():
    app = QtGui.QApplication(sys.argv)
    widget = TableWindow()
    widget.show()
    widget.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
