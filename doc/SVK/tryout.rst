Download into the folder "local_data copies"

run "snakemake -j 8 results/networks/elec_s_212_ec_lv1_1H.nc"

run jupyter notebook
There, go to folder "ipynb_checkpoints"
run the cells in tryout.ipynb one by one

(you probably have to change the path to the network. For me it is
n= pypsa.Network("/home/slvst/PycharmProjects/pypsa-eur/results/networks/elec_s_212_ec_lv1_1H.nc") )
