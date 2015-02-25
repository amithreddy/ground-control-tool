import mock
import main

def mocksqldb():
    return mock.create_autospec(main.sqldb)

class yes_no(mock.Mock):
    def __init__(self):
        self.Yes =True
        self.No = False
        self.question.return_value=True


