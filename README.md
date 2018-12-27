# dir_from_chamo

This project was written for the University of Warsaw Library. It's main aim is to facillitate creating directories for scans of publications.
The program connects with CHAMO, retrives needed data and creates one or more directories.

Example of command line call:
```
python -m src.main.python.main.py <dir in whom dir will be created>
```

If in directory given as parameter there is `directories.txt` file with list of values for 035 field from MARC format, program will create directories for all of them. Otherwise user will be asked for system number.
