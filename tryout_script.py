import pypsa
import matplotlib.pyplot as plt
from icecream import ic
import os
from os.path import normpath, exists
os.path.isdir("/pypsa-eur")
os.getcwd()
ic(os.getcwd())
n= pypsa.Network("/home/slvst/PycharmProjects/pypsa-eur/"
                 "networks/elec_s_335_ec_lv1_1H.nc")
ic(n.plot())