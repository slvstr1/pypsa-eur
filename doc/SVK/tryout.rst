Download into the folder "local_data copies"
    print("you need to manually download the following files and put them in the folder local_data_copies")
    print("https://zenodo.org/record/3517935/files/pypsa-eur-data-bundle.tar.xz")
    print("https://sdi.eea.europa.eu/datashare/s/H6QGCybMdLLnywo/download")
    print("and unzip the zip archive 'eea_v_3035_100_k_natura2000_p_2020_v11_r00.zip'")
    print("and move the file 'Natura2000_end2020.gpkg' out of the archive inside the archive 'eea_v_3035_100_k_natura2000_p_2020_v11_r00'")

    print("https://data.open-power-system-data.org/time_series/2019-06-05/time_series_60min_singleindex.csv")
    print("https://zenodo.org/record/6382570/files/europe-2013-era5.nc")
    print("https://zenodo.org/record/6382570/files/europe-2013-sarah.nc")

run "snakemake -j 4 results/networks/elec_s_212_ec_lv1_1H.nc"
(5 minutes on my desktop machine!!! - probably somewhat more on yours - maybe 10~20?)

run jupyter notebook
    There, go to folder "ipynb_checkpoints"
    run the cells in tryout.ipynb one by one

    (you probably have to change the path to the network. For me it is
    n= pypsa.Network("/home/slvst/PycharmProjects/pypsa-eur/results/networks/elec_s_212_ec_lv1_1H.nc") )
