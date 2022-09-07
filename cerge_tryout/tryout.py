import pypsa
import matplotlib.pyplot as plt
from icecream import ic

for i in range(16,26):
    n= pypsa.Network(f"/home/slvst/PycharmProjects/pypsa-eur/results/networks/elec_s_{i}_ec_lv1_1H"
                     f".nc")
    fig, ax = plt.subplots()
    fig=n.plot()
    plt.show()

# fig, ax = plt.subplots(n)
# fig.show()
# t.show()
fig = plt.figure()

show_outcomes_buses_keys =['p','marginal_price']
show_outcomes_lines_keys=['mu_upper', 'mu_lower']
print()

# ic(f"to show: {show_outcomes_buses_keys}")
# ic(list(network.buses_t[x] for x in show_outcomes_buses_keys))
# ic(list(n.lines_t[x] for x in show_outcomes_lines_keys))
print()
print()
# ic(list(n.buses_t[x] for x in show_outcomes_buses_keys))
# ic(n.buses_t['marginal_price'][:0])
# cz_bool =list ('CZ0' in elta for elta in n.buses_t)
# ic(cz_bool)
# ic(n.buses_t)
# ic(type(n.buses_t))
#
# ic(n.buses_t[cz_bool])
# ic(cz_indices)

# spike_cols = [col for col in n.buses if 'CZ' in col]
# ic(spike_cols)
cz_cols = [col for col in n.buses[0:] ]
ic(cz_cols)
ic(list('CZ' in col for col in n.buses.index))
cz_bus = n.buses.loc[('CZ' in col for col in n.buses.index)]
ic( cz_bus)
mp_t = n.buses_t['marginal_price']
ic(mp_t)
ic(type(mp_t))
mp_t.to_excel("output.xlsx")
cz_cols_t = [col for col in mp_t]
ic(cz_cols_t)
# ic(type(n.buses_t))
# ic(n.buses_t.items())
# cz_bus_t = n.buses_t.loc[('CZ' in col for col in n.buses.index)]
# ic( cz_bus_t)
# ic( n.buses_t)
# ic(type(n.buses_t))
# cz_list=(list(i for i in n.buses.country if i=='CZ'))
# ic(cz_list)
# ic(len(cz_list))


# ax = plt.axes(c=n.plot())
#
# for c in n.iterate_components(list(n.components.keys())[2:]):
#     print(f"Comp {c.name} has {len(c.df)} entries")
#
# print(n.snapshots)
# ic(n.lines.head())
# ic(n.generators.head())
# ic(n.storage_units.head())
# ic(n.loads.head())
# ic(n.loads_t)
# ic(n.loads_t.p_set.head())
#
#
# fig, ax = plt.subplots()
# ax=n.loads_t.p_set.sum(axis=1).plot()
# plt.show()
#
#
# ic(n.generators.p_max_pu)
# ic(n.generators_t.p_max_pu)
# ic(n.generators_t.p_max_pu.loc['2013-03', 'BE0 0 onwind'].plot())
# w=n.generators_t.p_max_pu.loc['2013-03', 'BE0 0 onwind'].plot()
# plt.show()
# w=n.generators_t.p_max_pu.loc['2013-03', 'BE0 0 solar'].plot()
# plt.show()
# ic(n.objective / 1e9)
# ic(n.lines.s_nom_opt,n.lines.s_nom, (n.lines.s_nom_opt-n.lines.s_nom).head())
# ic(n.generators.groupby("carrier").p_nom_opt.sum()/1e3)
# ic(n.storage_units.groupby("carrier").p_nom_opt.sum()/1e3)