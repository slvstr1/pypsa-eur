# SPDX-FileCopyrightText: : 2017-2020 The PyPSA-Eur Authors
#
# SPDX-License-Identifier: MIT

# coding: utf-8
"""
Adds dynamic line rating timeseries to the base network.

Relevant Settings
-----------------

.. code:: yaml

    lines:
        cutout:
        line_rating:


.. seealso::
    Documentation of the configuration file ``config.yaml`
Inputs
------

- ``data/cutouts``: 
- ``networks/base.nc``: confer :ref:`base`

Outputs
-------

- ``resources/line_rating.nc``


Description
-----------

The rule :mod:`build_line_rating` calculates the line rating for transmission lines. 
The line rating provides the maximal capacity of a transmission line considering the heat exchange with the environment. 

The folloing heat gains and losses are considered:

- heat gain through resistive losses
- heat gain trough solar radiation
- heat loss through radiation of the trasnmission line
- heat loss through forced convection with wind
- heat loss through natural convection 


With a heat balance considering the maximum temperature threshold of the tranmission line, 
the maximal possible capacity factor "s_max_pu" for each transmission line at each time step is calculated.
"""

import logging
from _helpers import configure_logging

import pypsa
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString as Line
import atlite
import xarray as xr
import re

def calculate_resistance(T, R_ref, T_ref=20, alpha=0.00403):
    """
    Calculates the resistance at other temperatures than the reference temperature.

    Parameters
    ----------
    T : Temperature at which resistance is calculated in [°C] or [K]
    R_ref : Resistance at reference temperature in [Ohm] or [Ohm/Per Length Unit]
    T_ref : Reference temperature in [°C] or [K]
    alpha: Temperature coefficient in [1/K]
        Defaults are:
            * T_ref : 20 °C
            * alpha : 0.00403 1/K

    Returns
    -------
    Resistance of at given temperature.
    """
    R=R_ref+(1+alpha*(T-T_ref))
    return R

def calculate_line_rating(n):
    """
    Calculates the maximal allowed power flow in each line for each time step considering the maximal temperature.

    Parameters
    ----------
    n : pypsa.Network object containing information on grid
    
    Returns
    -------
    xarray DataArray object with maximal power.
    """
    relevant_lines=n.lines[(n.lines['underground']==False) & (n.lines['under_construction']==False)] 
    buses = relevant_lines[["bus0", "bus1"]].values
    x = n.buses.x
    y = n.buses.y
    shapes = [Line([Point(x[b0], y[b0]), Point(x[b1], y[b1])]) for (b0, b1) in buses]
    shapes = gpd.GeoSeries(shapes, index=relevant_lines.index)
    cutout = atlite.Cutout(snakemake.input.cutout)
    if relevant_lines.r_pu.eq(0).all():
        #Overwrite standard line resistance with line resistance obtained from line type 
        relevant_lines["r_pu"]=relevant_lines.join(n.line_types["r_per_length"], on=["type"])['r_per_length']/1000 #in meters
        #Set default number of bundles per line
        relevant_lines["n_bundle"]=1
        #If line type with bundles is given retrieve number of conductors per bundle
        if relevant_lines["type"].str.contains("bundle").all():
            relevant_lines["n_bundle"]=relevant_lines["type"].apply(lambda x: int(re.findall(r"(\d+)-bundle", x)[0]))
    Imax=cutout.line_rating(shapes, relevant_lines.r_pu, D=0.0218 ,Ts=353 , epsilon=0.8, alpha=0.8)
    da = xr.DataArray(data=np.sqrt(3) * Imax * relevant_lines["v_nom"].values.reshape(-1,1) * np.sqrt(relevant_lines["n_bundle"].values.reshape(-1,1)) * relevant_lines["num_parallel"].values.reshape(-1,1)/1e3, #in mW
                      attrs=dict(description="Maximal possible power in MW for given line considering line rating"))
    return da

if __name__ == "__main__":
    if 'snakemake' not in globals():
        from _helpers import mock_snakemake
        snakemake = mock_snakemake('build_line_rating', network='elec', simpl='',
                                  clusters='6', ll='copt', opts='Co2L-24H')
    configure_logging(snakemake)

    n = pypsa.Network(snakemake.input.base_network)  
    da=calculate_line_rating(n)

    da.to_netcdf(snakemake.output[0])