# Copyright 2019-2022 Fabian Hofmann (TUB, FIAS)
# SPDX-FileCopyrightText: : 2017-2022 The PyPSA-Eur Authors
#
# SPDX-License-Identifier: MIT

"""
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3517935.svg
   :target: https://doi.org/10.5281/zenodo.3517935

The data bundle (1.4 GB) contains common GIS datasets like NUTS3 shapes, EEZ shapes, CORINE Landcover, Natura 2000 and also electricity specific summary statistics like historic per country yearly totals of hydro generation, GDP and POP on NUTS3 levels and per-country load time-series.

This rule downloads the data bundle from `zenodo <https://doi.org/10.5281/zenodo.3517935>`_ and extracts it in the ``data`` sub-directory, such that all files of the bundle are stored in the ``data/bundle`` subdirectory.

The :ref:`tutorial` uses a smaller `data bundle <https://zenodo.org/record/3517921/files/pypsa-eur-tutorial-data-bundle.tar.xz>`_ than required for the full model (188 MB)

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3517921.svg
    :target: https://doi.org/10.5281/zenodo.3517921

**Relevant Settings**

.. code:: yaml

    tutorial:

.. seealso::
    Documentation of the configuration file ``config.yaml`` at
    :ref:`toplevel_cf`

**Outputs**

- ``data/bundle``: input data collected from various sources

"""

import logging
import tarfile
from pathlib import Path
import os
from shutil import copyfile

from _helpers import configure_logging, progress_retrieve

logger = logging.getLogger(__name__)

# from .SVK_edits
# from local_switch import use_local_data_copies

# print(use_local_data_copies)
if __name__ == "__main__":
    if "snakemake" not in globals():
        from _helpers import mock_snakemake

        snakemake = mock_snakemake("retrieve_databundle")
        rootpath = ".."
    else:
        rootpath = "."

    use_local_data_copies = snakemake.config['use_local_data_copies']
    local_data_copies_path = snakemake.config['local_data_copies_path_name']

    configure_logging(
        snakemake
    )  # TODO Make logging compatible with progressbar (see PR #102)

    if snakemake.config["tutorial"]:
        url = "https://zenodo.org/record/3517921/files/pypsa-eur-tutorial-data-bundle.tar.xz"
    else:
        url = "https://zenodo.org/record/3517935/files/pypsa-eur-data-bundle.tar.xz"
        rootpath = '.'
    configure_logging(snakemake) # TODO Make logging compatible with progressbar (see PR #102)


    use_local_data_copies = snakemake.config['use_local_data_copies']
    local_data_copies_path= snakemake.config['local_data_copies_path_name']

    # Save locations


    tarball_fn = Path(f"{rootpath}/bundle.tar.xz")
    to_fn = Path(f"{rootpath}/data")


    if snakemake.config['tutorial']:
        url = "https://zenodo.org/record/3517921/files/pypsa-eur-tutorial-data-bundle.tar.xz"
        progress_retrieve(url, tarball_fn)

    else:

        # SVK edits start

        path_to_local_file = os.path.join(local_data_copies_path, "pypsa-eur-data-bundle.tar.xz")
        file_exists = os.path.exists(path_to_local_file)


        if use_local_data_copies and file_exists:
            # tarball_fn= Path(f"{rootpath}/local_data_copies/pypsa-eur-data-bundle.tar.xz")
            tarball_fn = path_to_local_file
            # Path("local_data_copies/pypsa-eur-data-bundle.tar.xz")
            url = tarball_fn
            logger.info(f"Getting databundle locally from '{url}'.")
            # progress_retrieve(url, tarball_fn)

        else:
            url = "https://zenodo.org/record/3517935/files/pypsa-eur-data-bundle.tar.xz"
            tarball_fn = Path(f"{rootpath}/local_data_copies/pypsa-eur-data-bundle.tar.xz")


            progress_retrieve(url, tarball_fn)
            logger.info(f"Downloading databundle from '{url}'.")
            if use_local_data_copies:
                copyfile(tarball_fn, path_to_local_file)
        # SVK edits end

    # logger.info(f"Downloading databundle from '{url}'.")
    # progress_retrieve(url, tarball_fn)




    logger.info(f"Extracting databundle.")
    tarfile.open(tarball_fn).extractall(to_fn)

    # SVK edit (why would you delete it? delete = next time a new 1.6GB download)
    # tarball_fn.unlink()

    logger.info(f"Databundle available in '{to_fn}'.")
    print("in databundle!")
