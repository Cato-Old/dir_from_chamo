import os
import sys
import tkinter
from tkinter import simpledialog
from src.main.python.dataretrive import ChamoRequest, MARCFormatter


def run():
    current_dir = sys.argv[1]
    if os.path.exists(current_dir + 'directories.txt'):
        with open(current_dir + 'directories.txt') as f:
            dir_ls = [x[:-1] for x in f.readlines()]
    else:
        tkinter.Tk().withdraw()
        dir_ls = [simpledialog.askstring('035', 'Wprowadź wartość pola 035 formatu MARC: ')]
    chreq_ls = (MARCFormatter(ChamoRequest(x).get_data()).data_format() for x in dir_ls)
    for chreq in chreq_ls:
        os.mkdir(current_dir + chreq)


run()
