# Symbolic-Methods-FAERS-Project
Pulls entries from FAERS database, automatically maps them to concepts in SNOMED-CT and RxNorm

Python version = 3.9.12


example query URL:
https://api.fda.gov/drug/event.json?search=(receivedate:[20190601+TO+20190601])AND+primarysource.reportercountry=FR&limit=10


some source code taken from here:
https://github.com/neksa/openfda-faers/blob/master/OpenFDA%20API%20for%20FAERS.ipynb
