from PyQt4 import QtCore
match= r'(?:[-+]?(\d+(\.\d+)?|(\.\d+)))'
match_nums= QtCore.QRegExp( '^'+match+r'[,]'\
                            + match+r'[,]'\
                            + match+'$')
match_one_num = QtCore.QRegExp('^'+match+'$')
