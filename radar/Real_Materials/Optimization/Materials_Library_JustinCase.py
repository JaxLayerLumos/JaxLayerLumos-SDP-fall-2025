materials_data = [
    { 
        'name': "Alumina 99.5% dense (1–250 GHz)", 
        'section': 1, 
        'freq_range_ghz': (1, 250),
        'eps_params': {
            'B': 2.399 + 0.0001j, 
            'C': 2.399 + 0.0001j, 
            'D': 0.000122 - 0.0000193j, 
            'G': 2.40 + 0.0001j, 
            'H': -0.00000693 - 0.00000375j, 
            'I': 0.0000133 + 0.00000231j, 
            'J': -0.0000000562 + 0.0000000326j}
    },
    { 
        'name': "Alumina 99.9% dense 3.86–3.90 g/cc (1–300 GHz)", 
        'section': 1, 
        'freq_range_ghz': (1, 300),
        'eps_params': {
            'B': 2.3945 + 0.0033j, 
            'C': 2.3985 + 0.0032j, 
            'D': 0.0243 + 0.001j, 
            'G': 2.39 + 0.0034j, 
            'H': 0.0005 + 0.0007j, 
            'I': 0.0001 + 0.000000294j, 
            'J': 0.00000230 + 0j}
    },
    { 
        'name': "SRM709 (0.01–18 GHz), Lead oxide glass", 
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 4.0907 + 0.0174j, 
            'C': 4.0907 + 0.0174j, 
            'D': -0.0002 + 0.0031j, 
            'G': 4.0902 + 0.0168j, 
            'H': -0.0001 + 0.0014j, 
            'I': 0.0074 + 0.004j, 
            'J': 0.0005 + 0.0006j}
    },
    { 
        'name': "Mullite 97% dense (2–35 GHz), 3 Al2O3 • 2SiO2", 
        'section': 1, 
        'freq_range_ghz': (2, 35),
        'eps_params': {
            'B': 1.6387 + 0.0007j, 
            'C': 1.6387 + 0.0007j, 
            'D': -0.0001 + 0.0001j, 
            'G': 1.6387 + 0.0007j, 
            'H': -0.0000216 + 0.0000142j, 
            'I': 0.0000114 + 0.0000309j, 
            'J': -0.000000463 + 0.000000863j}
    },
    { 
        'name': "Magnesium oxide (MgO) (2–35 GHz)", 
        'section': 1, 
        'freq_range_ghz': (2, 35),
        'eps_params': {
            'B': 2.3743 + 0.0003j, 
            'C': 2.3743 + 0.0003j, 
            'D': 0.0024 + 0.0003j, 
            'G': 2.3743 + 0.0001j, 
            'H': -0.0004 + 0.000000591j, 
            'I': 0 + 0.0000000175j, 
            'J': 0 + 0j}
    },
    { 
        'name': "Slip-cast silica, 2.05 g/cc (2–35 GHz)",
        'section': 1, 
        'freq_range_ghz': (2, 35),
        'eps_params': {
            'B': 0.8174 + 0.0001j, 
            'C': 0.8174 + 0.0001j, 
            'D': 0.0012 + 0.0001j, 
            'G': 0.8174 + 0.0001j, 
            'H': -0.0002 + 0.0001j, 
            'I': -0.0000121 + 0.000356j, 
            'J': 0.00000362 + 0.00000133j}
    },
    { 
        'name': "Shuttle tile FRIC12 (3–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (3, 100),
        'eps_params': {
            'B': 0.2741 + 0.0006j, 
            'C': 0.2741 + 0.0006j, 
            'D': -0.04 + 0.0008j, 
            'G': 0.2755 + 0.0005j, 
            'H': -0.0031 + 0.0001j, 
            'I': 0.0001 - 0.0003j, 
            'J': -0.0000139 - 0.00000036j}
    },
    { 
        'name': "Beryllium oxide (BeO) (0.2–250 GHz)",
        'section': 1, 
        'freq_range_ghz': (0.2, 250),
        'eps_params': {
            'B': 1.6503 + 0.0001j, 
            'C': 1.6503 + 0.0001j, 
            'D': -0.0023 + 0.0001j, 
            'G': 1.6502 - 0.00000102j, 
            'H': 0.00001042 - 0.000357j, 
            'I': 0.000002546 - 0.0000000109j, 
            'J': -0.00000184 + 0j}
    },
    { 
        'name': "Boron nitride; 2.28 g/cc (1–40 GHz) (Nominal εr = 4.08, Accumet Engineering)",
        'section': 1, 
        'freq_range_ghz': (1, 40),
        'eps_params': {
            'B': 1.1255 + 0.0002j, 
            'C': 1.1255 + 0.0002j, 
            'D': 0.0001 + 0.0006j, 
            'G': 1.1255 + 0.0002j, 
            'H': 0.0001 + 0.0001j, 
            'I': 0.0001 - 0.0011j, 
            'J': 0.00000502 + 0.00000504j}
    },
    { 
        'name': "SRM 709 Lead-oxide glass (0.01–18 GHz)",
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 4.0905 + 0.0173j, 
            'C': 4.0905 + 0.0173j, 
            'D': -0.0002 + 0.0031j, 
            'G': 4.0905 + 0.0175j, 
            'H': -0.0001 + 0.0014j, 
            'I': 0.0074 + 0.004j, 
            'J': 0.0005 + 0.0006j}
    },
    { 
        'name': "SRM 710a Sodalime glass (0.01–18 GHz)",
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 1.7687 + 0.0004j,
            'C': 1.7687 + 0.0004j, 
            'D': -0.0024 - 0.0003j, 
            'G': 1.7687 + 0.0004j, 
            'H': -0.0004 + 0.0015j, 
            'I': 0.0017 - 0.0006j, 
            'J': -0.0001 + 0.0001j}
    },
    { 
        'name': "PyroCeram (2–40 GHz)",
        'section': 1, 
        'freq_range_ghz': (2, 40),
        'eps_params': {
            'B': 1.4171 + 0.0003j, 
            'C': 1.4171 + 0.0003j, 
            'D': -0.0002 + 0.0003j, 
            'G': 1.4171 - 0.0000137j, 
            'H': -0.000000194 - 0.000154j, 
            'I': 0.00000174 + 0.0000328j, 
            'J': -0.00000236 + 0j}
    },
    { 
        'name': "Silicon nitride 3.2–3.3 g/cc (2–35 GHz)",
        'section': 1, 
        'freq_range_ghz': (2, 35),
        'eps_params': {
            'B': 1.3598 + 0.0024j, 
            'C': 1.36 + 0.0025j, 
            'D': 0.0115 + 0.0001j, 
            'G': 1.3599 + 0.0025j, 
            'H': 0.001 - 0.0008j, 
            'I': -0.0014 + 0.00000461j, 
            'J': 0.0000596 + 0j}
    },
    { 
        'name': "Fused silica-glass (Dynasil 4000) (2–40 GHz)",
        'section': 1, 
        'freq_range_ghz': (2, 40),
        'eps_params': {
            'B': 0.9688 + 0.0001j, 
            'C': 0.9688 + 0.0001j, 
            'D': -0.0012 + 0.0001j, 
            'G': 0.9688 + 0.0001j, 
            'H': 0.0002 + 0.0002j, 
            'I': -0.000012161 - 0.0000467j, 
            'J': -0.00000715 + 0.000000633j}
    },
    { 
        'name': "Fused silica glass (Dynasil 4000, 2.16–2.2 g/cc) (0.1–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (0.1, 100),
        'eps_params': {
            'B': 0.9469 + 0.0001j, 
            'C': 0.9469 + 0.0001j, 
            'D': -0.0081 + 0.0001j, 
            'G': 0.9468 - 0.000000074j, 
            'H': -0.0003 + 0j, 
            'I': -0.0019 + 0j, 
            'J': -0.0000335 + 0j}
    },
    { 
        'name': "Spinel magnesium aluminum oxide (MgAl2O4) (2–35 GHz)",
        'section': 1, 
        'freq_range_ghz': (2, 35),
        'eps_params': {
            'B': 2.0614 + 0.0004j, 
            'C': 2.0615 + 0.0004j, 
            'D': 0.0098 + 0.0001j, 
            'G': 2.0614 + 0.0004j, 
            'H': 0.002 + 0.00000107j, 
            'I': 0.0022 + 0j, 
            'J': 0.0000864 + 0j}
    },
    { 
        'name': "Magnesium titanate 16 (0.01–18 GHz) (Nominal εr = 16)",
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 4.2136 + 0.0099j, 
            'C': 4.2131 + 0.0099j, 
            'D': 0.0094 + 0.0055j, 
            'G': 4.2135 + 0.0099j, 
            'H': 0.0073 + 0.0007j, 
            'I': 0.0085 + 0.0046j, 
            'J': 0.0004 + 0.0011j}
    },
    {
        'name': "80 µm 9%/vol in epoxy, 1.38 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 18),
        'chi_m_params': {
            'B': 0.34, 
            'C': 1.8694, 
            'D': 0.8412},
        'eps1_params': None,
        'eps2_params': {
            'B': 2.47+0.26j, 
            'C': 8E-02-0.14j, 
            'D': 0.61+0.68j, 
            'E': -0.17+0.48j, 
            'F': 0.66-7E-02j, 
            'G': 10.66-12.9j, 
            'H': -18.6+10.47j}
    },
    {
        'name': "80 µm 16%/vol in epoxy, 1.6 g/cc",
        'section': 4,
        'freq_range_ghz': (0.001, 10),
        'chi_m_params': {
            'B': 1.16, 
            'C': 0.6562, 
            'D': 0.2022},
        'eps1_params': None,
        'eps2_params': {
            'B': 2.66+0.16j, 
            'C': 7E-02-9E-02j, 
            'D': 0.61+0.39j, 
            'E': 0.26+0.42j, 
            'F': 0.81+0.12j, 
            'G': 4.3+10.9j, 
            'H': 51.6+43.9j}
    },
    {
        'name': "80 µm 16.7%/vol in epoxy, 1.68 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 1.23, 
            'C': 1.499, 
            'D': 0.583},
        'eps1_params': {
            'B': 1.57+5E-02j, 
            'C': 9E-02+0.14j, 
            'D': -1.7-0.25j, 
            'E': 1.71+0.12j, 
            'F': 5E-02-14.7j, 
            'G': 1.52+43.6j},
        'eps2_params': None
    },
    {
        'name': "80 µm 29.9%/vol in epoxy, 2.22 g/cc (0.05-10 GHz)",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 2.21, 
            'C': 0.866, 
            'D': 0.940},
        'eps1_params': None,
        'eps2_params': None
    },
    {
        'name': "80 µm 29.9%/vol in epoxy, 2.22 g/cc (0.001-18 GHz)",
        'section': 4,
        'freq_range_ghz': (0.001, 18),
        'chi_m_params': {
            'B': 2.04, 
            'C': 0.554, 
            'D': 0.240},
        'eps1_params': {
            'B': 2.57+0.55j, 
            'C': 1.46+0.56j, 
            'D': -3e-3-4e-3j, 
            'E': -0.44-1.1j, 
            'F': 20.16+7.5j, 
            'G': -11.9-73.9j},
        'eps2_params': None
    },
    {
        'name': "80 µm 41.1%/vol in epoxy, 2.68 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 4.15, 
            'C': 0.61, 
            'D': 0.28},
        'eps1_params': {
            'B': 1.18+4e-2j, 
            'C': 1.14+3e-2j, 
            'D': -9e-2+5e-2j, 
            'E': 1.26+4e-2j, 
            'F': 13.8-13.7j, 
            'G': 6.03+90.4j},
        'eps2_params': None
    },
    {
        'name': "80 µm 49.4%/vol in epoxy, ~3.0 g/cc",
        'section': 4,
        'freq_range_ghz': (0.001, 10),
        'chi_m_params': {
            'B': 6.18, 
            'C': 0.33, 
            'D': 0.12},
        'eps1_params': {
            'B': 1.75+7e-2j, 
            'C': 1.58+0.18j, 
            'D': -0.23+3e-2j, 
            'E': 1.85+0.16j, 
            'F': 14.68-10.64j, 
            'G': -34.2+15.8j},
        'eps2_params': {
            'B': 3.23+0.44j, 
            'C': 0.07+0.11j, 
            'D': 0.65+0.42j, 
            'E': -0.95+0.1j, 
            'F': 1.96+0.17j, 
            'G': 7.53-3.33j, 
            'H': -10.26-4.8j}
    },
    {
        'name': "80 µm 53.6%/vol in epoxy, ~3.2 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 4.72, 
            'C': 0.7178, 
            'D': 0.3421},
        'eps1_params': {
            'B': 1.63-2E-02j, 
            'C': 1.47+7E-02j, 
            'D': -5E-002-0.17j, 
            'E': 1.89-2E-002j, 
            'F': 1.64+13.67j, 
            'G': 14.2+22.1j},
        'eps2_params': {
            'B': 3.28+2E-002j, 
            'C': 0.31-9E-002j, 
            'D': 0.39+0.3j, 
            'E': -0.94+0.63j, 
            'F': 1.72-2E-003j, 
            'G': 7.89+9.44j, 
            'H': 6.18-49.19j}
    },
    {
        'name': "80 µm 58.4%/vol in epoxy, ~3.29 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 8.86, 
            'C': 0.34, 
            'D': 0.12},
        'eps1_params': {
            'B': 1.2-1.4j, 
            'C': 1.9-0.98j, 
            'D': -0.12-0.16j, 
            'E': 2.05+2.73j, 
            'F': 7.32-15.6j, 
            'G': -33.7+20.6j},
        'eps2_params': {
            'B': 3.49+0.18j, 
            'C': 0.6-0.16j, 
            'D': 0.34-3.7E-002j, 
            'E': -0.74+0.72j, 
            'F': 2.29+2E-002j, 
            'G': 2.87+2.01j, 
            'H': 0.9-2.7j}
    },
    {
        'name': "80 µm 61.4%/vol in epoxy, ~3.52 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 10.69, 
            'C': 0.403, 
            'D': 0.18},
        'eps1_params': {
            'B': 1.89-1.31j, 
            'C': 2.63-0.85j, 
            'D': -0.12-0.18j, 
            'E': 2.72+2.88j, 
            'F': 14.49-13.49j, 
            'G': -48.4+18.1j},
        'eps2_params': {
            'B': 3.96+0.33j, 
            'C': 1.05-0.11j, 
            'D': 9E-002-0.2j, 
            'E': -1.02+0.82j, 
            'F': 2.9+0.4j, 
            'G': 8.7-2.2j, 
            'H': -3.12-11.9j}
    },
    {
        'name': "80 µm 61.8%/vol in epoxy, ~3.53 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 7.50, 
            'C': 0.55, 
            'D': 0.26},
        'eps1_params': {
            'B': 1.88-1.35j, 
            'C': 2.1-0.62j, 
            'D': -8E-002-0.22j, 
            'E': 2.54+2.62j, 
            'F': 15.88-23.4j, 
            'G': -54.1+17.5j},
        'eps2_params': {
            'B': 3.85+0.25j, 
            'C': 0.95-0.15j, 
            'D': 0.33-0.28j, 
            'E': -1.04+0.65j, 
            'F': 2.79+0.14j, 
            'G': 7.3-0.23j, 
            'H': 1.48-5.1j}
    },
    {
        'name': "80 µm 76.1%/vol in epoxy, ~4.12 g/cc",
        'section': 4,
        'freq_range_ghz': (0.001, 10),
        'chi_m_params': {
            'B': 14.20, 
            'C': 0.18, 
            'D': 0.053},
        'eps1_params': None,
        'eps2_params': None
    },
    {
        'name': "500-nm Fe 7% + 80-µm Ferrite 7%/vol in epoxy, 1.8 g/cc",
        'section': 4,
        'freq_range_ghz': (0.001, 18),
        'chi_m_params': {
            'B': 1.05, 
            'C': 3.32, 
            'D': 1.68},
        'eps1_params': {
            'B': 3.31+0.11j, 
            'C': 2.32+0.15j, 
            'D': 5e-3-6e-3j, 
            'E': 1.87-0.22j, 
            'F': 12.1-0.76j, 
            'G': -2.2-19.8j},
        'eps2_params': {
            'B': 3.93+2e-2j, 
            'C': 0.97-0.13j, 
            'D': 3e-2+0.15j, 
            'E': -0.26+0.32j, 
            'F': 2.8+0.16j, 
            'G': 13.1-2.91j, 
            'H': -11.8-19j}
    },
    {
        'name': "500-nm Fe 10.2% + 80-µm Ferrite 10.1%/vol in epoxy, 2.1 g/cc",
        'section': 4,
        'freq_range_ghz': (0.001, 10),
        'chi_m_params': {
            'B': 0.99, 
            'C': 4.12, 
            'D': 1.52},
        'eps1_params': {
            'B': 0.97-1.54j, 
            'C': 2.29+1.25j, 
            'D': 0.11-6E-002j, 
            'E': 2.1+2.69j, 
            'F': 8.39+13.31j, 
            'G': 18.7+15.7j},
        'eps2_params': None
    },
    {
        'name': "500-nm Fe 13.4% + 80-µm Ferrite 13.6%/vol in epoxy, 2.43 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 3.04, 
            'C': 1.87, 
            'D': 0.403},
        'eps1_params': {
            'B': 1.4+1.37j,
            'C': 2.76-1.06j, 
            'D': 0+2E-002j, 
            'E': 2.45+2.9j, 
            'F': 266.8-266.9j, 
            'G': -24.8-26.1j},
        'eps2_params': {
            'B': 3.53+0.2j, 
            'C': 0.92-0.75j, 
            'D': 0.29+0.14j, 
            'E': 0.44+4E-002j, 
            'F': 2.92+0.2j, 
            'G': 11.6-12j, 
            'H': -34.8+6.3j}
    },
    {
        'name': "500-nm Fe 17.5% + 80-µm Ferrite 17.5%/vol in epoxy, 2.82 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 4.86, 
            'C': 0.954, 
            'D': 0.3640},
        'eps1_params': {
            'B': 2.08-0.82j, 
            'C': 3.16-0.69j, 
            'D': 0.28+9E-002j, 
            'E': 5.78+2.28j, 
            'F': 4.2+0.3j, 
            'G': 1.26-2.32j},
        'eps2_params': {
            'B': 4.3+0.26j, 
            'C': 1.13-0.86j, 
            'D': -0.18-0.1j, 
            'E': 0.57+0.11j, 
            'F': 3.47+0.25j, 
            'G': 2-16.1j, 
            'H': -0.32+22.9j}
    },
    {
        'name': "500-nm Fe 19.9% + 80-µm Ferrite 20.0%/vol in epoxy, 3.1 g/cc",
        'section': 4,
        'freq_range_ghz': (0.001, 10),
        'chi_m_params': {
            'B': 8.14, 
            'C': 0.55, 
            'D': 0.21},
        'eps1_params': {
            'B': 2.41-1.8j, 
            'C': 3.27-1.2j, 
            'D': 8E-002+0.61j, 
            'E': 6.13+6.3j, 
            'F': 1.39+1.64j, 
            'G': 0.74-0.86j},
        'eps2_params': {
            'B': 3.67-4E-002j, 
            'C': 0.75-0.53j, 
            'D': -0.3-0.4j, 
            'E': -0.21+0.11j, 
            'F': 3.05-6E-002j, 
            'G': 23.64+12.3j, 
            'H': 16.3+5.2j}
    },
    {
        'name': "500-nm Fe 23.3% + 80-µm Ferrite 23.3%/vol in epoxy, 3.4 g/cc",
        'section': 4,
        'freq_range_ghz': (0.05, 10),
        'chi_m_params': {
            'B': 8.41, 
            'C': 0.525, 
            'D': 0.19},
        'eps1_params': {
            'B': 5.41+1.1j, 
            'C': 4-0.79j, 
            'D': -2E-003-2.6E-002j, 
            'E': -0.61+0.7j, 
            'F': 0.18+0.57j, 
            'G': 0.12+7E-002j},
        'eps2_params': {
            'B': 4.48+0.16j, 
            'C': 1.69-0.46j, 
            'D': -0.2-7E-002j, 
            'E': -0.62+0.11j, 
            'F': 3.65+8E-002j, 
            'G': 29.6-23.5j, 
            'H': -115+53.4j}
    },
    { 
        'name': "Zinc sulfide; 4.09 g/cc (3–240 GHz) (nominal εr = 8.5 at 2 MHz; Korth Kristalle GMBH)", 
        'section': 6, 
        'freq_range_ghz': (3, 240), 
        'eps_params': {
            'B': 2.44-0.006j, 
            'C': 2.58+0.006j, 
            'D': 0.15+0.006j, 
            'E': 0.15+0.006j, 
            'F': 1.9+0.003j, 
            'G': 3.5+53.24j, 
            'H': 18.9+88.9j},
    }, 
    { 
        'name': "Zinc selenide, 5.27 g/cc (5–240 GHz) (nominal εr = 8.98; Korth Kristalle GMBH)", 
        'section': 6, 
        'freq_range_ghz': (5, 240), 
        'eps_params': {
            'B': 2.37-0.13j, 
            'C': 2.65-0.04j, 
            'D': 0.15+0.07j, 
            'E': 0.14+0.06j, 
            'F': 2.53+0.06j, 
            'G': 136-138j, 
            'H': -176+42.4j},
    },
    { 
        'name': "Gallium arsenide (3–240 GHz) (nominal εr = 8.35–11.36; US pat. 6683510)", 
        'section': 6, 
        'freq_range_ghz': (3, 240), 
        'eps_params': {
            'B': 3.63-0.13j, 
            'C': 3.64-0.07j, 
            'D': 0.08+0.03j, 
            'E': 0.19-0.3j, 
            'F': 3.73-0.04j, 
            'G': 76.9-367j, 
            'H': -547+598j},
    },
    { 
        'name': "Germanium (5.33 g/cc) (3–10 GHz) (nominal εr = 16; Virginia Semiconductor)", 
        'section': 6, 
        'freq_range_ghz': (3, 10), 
        'eps_params': {
            'B': 11.97+2.83j, 
            'C': 13.23+3.4j, 
            'D': -0.02+0.25j, 
            'E': 0.53+1.44j, 
            'F': 14.53+1.8j, 
            'G': 1.1+6j, 
            'H': 0.92+8.12j},
    },
    {
        'name': "Epoxy, EAB (2–100 GHz), 1.24 g/cc",
        'section': 8,
        'freq_range_ghz': (2, 100),
        'eps_params': {
            'B': 1.0702+0.0532j,
            'C': 0.8609-0.0238j,
            'D': -0.5203+0.1529j,
            'G': 0.8918-0.0954j,
            'H': -0.002+0.0017j,
            'I': 0.0001-0.0048j,
            'J': -4.85E-005+5.91E-008j
        }
    },
    {
        'name': "1422, Cross-linked polystyrene 1.05 g/cc (4–100 GHz)",
        'section': 8,
        'freq_range_ghz': (4, 100),
        'eps_params': {
            'B': 0.5914+0.0509j,
            'C': 0.586+0.0483j,
            'D': 0.0224+0.0068j,
            'G': 0.7488-0.152j,
            'H': -0.0002+0.0013j,
            'I': -0.0014+0.0021j,
            'J': 2.74E-005+1.78E-005j
        }
    },
    {
        'name': "1000 Polyetherimide (2–60 GHz), 1.28 g/cc",
        'section': 8,
        'freq_range_ghz': (2, 60),
        'eps_params': {
            'B': 0.7855+0.0009j,
            'C': 0.7872+0.0008j,
            'D': -0.0293-0.0007j,
            'G': 0.7851+0.001j,
            'H': 0.0008+0.0001j,
            'I': 0.0001-0.0027j,
            'J': -4.51E-005-2.27E-006j
        }
    },
    {
        'name': "7058 Epoxy w/ ~40% vol silica hollow spheres (2–18 GHz)",
        'section': 8,
        'freq_range_ghz': (2, 18),
        'eps_params': {
            'B': 0.7275+0.0758j,
            'C': 2.4321+0.1323j,
            'D': -3.8007-0.9919j,
            'G': 1.6261+0.2312j,
            'H': -3.3603+1.9301j,
            'I': 0.9885-0.0586j,
            'J': -9E-003+0.0107j
        }
    }
]