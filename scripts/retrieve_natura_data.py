
import logging
from _helpers import progress_retrieve, configure_logging
import tarfile
from pathlib import Path
from os.path import exists, join
from shutil import copyfile

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    if 'snakemake' not in globals():
        from _helpers import mock_snakemake
        snakemake = mock_snakemake('retrieve_databundle')
        rootpath = '..'
    else:
        rootpath = '.'
    configure_logging(snakemake) # TODO Make logging compatible with progressbar (see PR #102)

    print("in natura_data retr")


    # Save locations
    tarball_fn = Path(f"{rootpath}/bundle.tar.xz")
    to_fn = Path(f"{rootpath}/data")


    if snakemake.config['tutorial']:
        url = "https://zenodo.org/record/3517921/files/pypsa-eur-tutorial-data-bundle.tar.xz"
        progress_retrieve(url, tarball_fn)

    else:


        # print(snakemake.config)
        use_local_data_copies = snakemake.config['use_local_data_copies']
        local_data_copies_path = snakemake.config['local_data_copies_path_name']
        path_to_file = join(local_data_copies_path, "pypsa-eur-data-bundle.tar.xz")
        file_exists = exists(path_to_file)
        print(f'use_local_data_copies{use_local_data_copies}')

        if not use_local_data_copies or not file_exists:
            url = "https://zenodo.org/record/3517935/files/pypsa-eur-data-bundle.tar.xz"
            progress_retrieve(url, tarball_fn)
            logger.info(f"Downloading databundle from '{url}'.")
            if use_local_data_copies:
                copyfile(tarball_fn, path_to_file)
        else:
            tarball_fn = path_to_file
            url = tarball_fn
            logger.info(f"Getting databundle locally from '{url}'.")



    # logger.info(f"Downloading databundle from '{url}'.")
    # progress_retrieve(url, tarball_fn)




    logger.info(f"Extracting databundle.")
    tarfile.open(tarball_fn).extractall(to_fn)
    tarball_fn.unlink()
    logger.info(f"Databundle available in '{to_fn}'.")
