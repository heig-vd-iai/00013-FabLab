#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication
from ui import Main


def main():
    app = QApplication(sys.argv)
    window = Main('MakerSpace Tools Extraction')
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
