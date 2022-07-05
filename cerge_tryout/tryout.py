import pypsa
import matplotlib.pyplot as plt
from icecream import ic

n= pypsa.Network("../results/networks/elec_s_6_ec_lcopt_Co2L-24H.nc")

# fig, ax = plt.subplots()
# fig=n.plot()

wcs = n.plot()
# import matplotlib
# fig = matplotlib.pyplot.figure()
# pyplot_2 = fig.add_subplot( projection=wcs)
plt.show()

# fig, ax = plt.subplots(n)
# fig.show()
# t.show()
fig = plt.figure()
# ax = plt.axes(c=n.plot())

for c in n.iterate_components(list(n.components.keys())[2:]):
    print(f"Comp {c.name} has {len(c.df)} entries")

print(n.snapshots)
ic(n.lines.head())
ic(n.generators.head())
ic(n.storage_units.head())
ic(n.loads.head())
ic(n.loads_t)
ic(n.loads_t.p_set.head())


fig, ax = plt.subplots()
ax=n.loads_t.p_set.sum(axis=1).plot()
plt.show()


ic(n.generators.p_max_pu)
ic(n.generators_t.p_max_pu)
ic(n.generators_t.p_max_pu.loc['2013-03', 'BE0 0 onwind'].plot())
w=n.generators_t.p_max_pu.loc['2013-03', 'BE0 0 onwind'].plot()
plt.show()
w=n.generators_t.p_max_pu.loc['2013-03', 'BE0 0 solar'].plot()
plt.show()
ic(n.objective / 1e9)
ic(n.lines.s_nom_opt,n.lines.s_nom, (n.lines.s_nom_opt-n.lines.s_nom).head())
ic(n.generators.groupby("carrier").p_nom_opt.sum()/1e3)
ic(n.storage_units.groupby("carrier").p_nom_opt.sum()/1e3)