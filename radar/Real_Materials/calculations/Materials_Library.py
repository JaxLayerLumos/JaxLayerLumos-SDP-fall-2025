materials_data = [
    { 
        'name': "3D Quartz–alumina silica nitride 2.16 g/cc (8–40 GHz)", 
        'section': 1, 
        'freq_range_ghz': (8, 40), 
        'eps_params': {
            'B': 0.9921 - 0.0001j, 
            'C': 1.0147 - 0.0004j, 
            'D': -0.0879 - 0.002j, 
            'G': 0.9732 - 0.0002j, 
            'H': 0.003 + 0.0004j, 
            'I': -0.0002 - 0.0076j, 
            'J': -0.000206 + 0.0000103j}
    },
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
            'I': 0.0000133 - 0.00000231j, 
            'J': -0.0000000562 + 0.0000000326j}
    },
    { 
        'name': "Alumina 99.9% dense 3.86–3.90 g/cc (1–300 GHz)", 
        'section': 1, 
        'freq_range_ghz': (1, 300),
        'eps_params': {
            'B': 2.3945 + 0.0033j, 
            'C': 2.3985 + 0.0032j, 
            'D': 0.0243 - 0.001j, 
            'G': 2.39 + 0.0034j, 
            'H': 0.0005 + 0j, 
            'I': 0.0001 + 0.0007j, 
            'J': 0.00000230 - 0.000000294j}
    },
    { 
        'name': "Alumina 96–97% dense, 3.71 g/cc (5–250 GHz)", 
        'section': 1, 
        'freq_range_ghz': (5, 250),
        'eps_params': {
            'B': 2.4313 + 0.0015j, 
            'C': 2.4285 + 0.0014j, 
            'D': 0.0112 - 0.00021j, 
            'G': 2.2536 - 0.0029j, 
            'H': 0.0004 + 0j, 
            'I': 0.0013 + 0j, 
            'J': 0.00000648 - 0.0000625j}
    },
    { 
        'name': "SRM709 (0.01–18 GHz), Lead oxide glass", 
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 4.0907 - 0.0174j, 
            'C': 4.0907 - 0.0174j, 
            'D': 0.0002 - 0.0031j, 
            'G': 4.0902 - 0.0168j, 
            'H': 0.0001 - 0.0014j, 
            'I': 0.0074 + 0.004j, 
            'J': 0.0005 - 0.0006j}
    },
    { 
        'name': "Mullite 97% dense (2–35 GHz), 3 Al2O3 • 2SiO2",
        'section': 1, 
        'freq_range_ghz': (2, 35),
        'eps_params': {
            'B': 1.6387 + 0.0007j, 
            'C': 1.6387 + 0.0007j, 
            'D': 0.0001 + 0.0001j, 
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
            'D': 0.0024 + 0j, 
            'G': 2.3743 + 0.0003j, 
            'H': 0.0004 - 0.0001j, 
            'I': 0.0005 + 0j, 
            'J': 0.0000175 + 0.000000591j}
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
            'H': -0.0002 - 0.0001j, 
            'I': -0.0000121 + 0.000356j, 
            'J': 0.00000362 + 0.00000133j}
    },
    { 
        'name': "Shuttle tile LI2200 (30–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (30, 100),
        'eps_params': {
            'B': 0.3371 + 0.0012j, 
            'C': 0.3371 + 0.0012j, 
            'D': -0.0026 - 0.0006j, 
            'G': 0.3374 + 0.0012j, 
            'H': 0.0005 - 0.0002j, 
            'I': 0.0001 + 0.0007j, 
            'J': 0.0000153 - 0.000000249j}
    },
    { 
        'name': "Shuttle tile FRIC12 (3–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (3, 100),
        'eps_params': {
            'B': 0.2741 + 0.0006j, 
            'C': 0.2741 + 0.0006j, 
            'D': -0.04 - 0.0008j, 
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
            'D': -0.0023 + 0j, 
            'G': 1.6502 + 0.0001j, 
            'H': 0.00001042 - 0.00000102j, 
            'I': 0.000002546 - 0.000357j, 
            'J': -0.00000184 - 0.0000000109j}
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
            'H': 0.0001 - 0.0001j, 
            'I': 0.0001 - 0.0011j, 
            'J': 0.00000502 + 0.00000504j}
    },
    { 
        'name': "Magnesium calcium titanate 30 (8–50 GHz) (Nominal εr = 30)",
        'section': 1, 
        'freq_range_ghz': (8, 50),
        'eps_params': {
            'B': -0.2585 + 0.0027j, 
            'C': 8.1811 + 0.5195j, 
            'D': 0.4159 + 0.3298j, 
            'G': 0.5493 + 0.0008j, 
            'H': -0.0024 + 0.0001j, 
            'I': -0.0216j, 
            'J': -0.0005 + 0j}
    },
    { 
        'name': "SRM 709 Lead-oxide glass (0.01–18 GHz)",
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 4.0905 - 0.0173j, 
            'C': 4.0905 - 0.0173j, 
            'D': 0.0002 - 0.0031j, 
            'G': 4.0905 - 0.0175j, 
            'H': 0.0001 - 0.0014j, 
            'I': 0.0074 + 0.004j, 
            'J': 0.0005 - 0.0006j}
    },
    { 
        'name': "SRM 710a Sodalime glass (0.01–18 GHz)",
        'section': 1, 
        'freq_range_ghz': (0.01, 18),
        'eps_params': {
            'B': 1.7687 - 0.0004j,
            'C': 1.7687 - 0.0004j, 
            'D': -0.0024 - 0.0003j, 
            'G': 1.7687 - 0.0004j, 
            'H': -0.0004 + 0.0015j, 
            'I': 0.0017 - 0.0006j, 
            'J': -0.0001 - 0.0001j}
    },
    { 
        'name': "PyroCeram (2–40 GHz)",
        'section': 1, 
        'freq_range_ghz': (2, 40),
        'eps_params': {
            'B': 1.4171 + 0.0003j, 
            'C': 1.4171 + 0.0003j, 
            'D': -0.0002 + 0j, 
            'G': 1.4171 - 0.0003j, 
            'H': -0.000000194 - 0.0000000137j, 
            'I': 0.00000174 + 0.00015427j, 
            'J': -0.00000236 - 0.0000000328j}
    },
    { 
        'name': "Sapphire wafer #1 (80–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (80, 100),
        'eps_params': {
            'B': 2.8008 + 0.0329j, 
            'C': 2.7989 + 0.039j, 
            'D': -0.0777 + 0.025j, 
            'G': 2.8204 + 0.0254j, 
            'H': 0.004 - 0.0012j, 
            'I': -0.0006 - 0.0046j, 
            'J': -0.0000493 + 0.0000053j}
    },
    { 
        'name': "Sapphire wafer #2 (80–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (80, 100),
        'eps_params': {
            'B': 2.4304 + 0.0426j, 
            'C': 2.4285 + 0.0414j, 
            'D': 0.0247 + 0.0237j, 
            'G': 2.4585 + 0.0476j, 
            'H': 0.0041 + 0.0032j, 
            'I': -0.0049 + 0.0027j, 
            'J': 0.0000272 + 0.0000404j}
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
            'I': 0.0014 + 0j, 
            'J': 0.0000596 + 0.00000461j}
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
            'D': -0.0081 + 0j, 
            'G': 0.9468 - 0.0001j, 
            'H': -0.0003 + 0j, 
            'I': -0.0019 + 0j, 
            'J': -0.0000335 + 0.000000074j}
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
            'H': 0.002 + 0j, 
            'I': 0.0022 + 0j, 
            'J': 0.0000864 + 0.00000107j}
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
        'name': "Barium titanate 38 (4.41–4.48 g/cc, 8–50 GHz) (Nominal εr = 38)",
        'section': 1, 
        'freq_range_ghz': (8, 50),
        'eps_params': {
            'B': 7.5015 + 0.0152j, 
            'C': 6.3603 + 0.0073j, 
            'D': 0.1914 + 0j, 
            'G': 8.0033 - 0.00436j, 
            'H': -0.0061 + 0.0002j, 
            'I': 0.0003 - 0.0174j, 
            'J': -0.0016 + 0j}
    },
    { 
        'name': "Cordierite (Mg2Al4Si5O18) (2.3–2.5 g/cc, 8–50 GHz)",
        'section': 1, 
        'freq_range_ghz': (8, 50),
        'eps_params': {
            'B': 1.2293 + 0.0119j, 
            'C': 1.5892 + 0.0023j, 
            'D': -0.2778 - 0.0336j, 
            'G': 1.6774 + 0.1004j, 
            'H': -0.0067 - 0.0035j, 
            'I': 0.0005 - 0.0022j, 
            'J': 0.0000443 + 0.0000005j}
    },
    { 
        'name': "Magnesium aluminum titanate 11 (3.3–3.5 g/cc, 8–50 GHz) (Nominal εr = 11)",
        'section': 1, 
        'freq_range_ghz': (8, 50),
        'eps_params': {
            'B': 2.3079 - 0.0325j, 
            'C': 2.5009 + 0.2874j, 
            'D': -0.1472 - 0.1533j, 
            'G': 1.7366 + 0.8388j, 
            'H': 0.0114 - 0.0319j, 
            'I': 0.012 - 0.0155j, 
            'J': -0.0003 - 0.0003j}
    },
    { 
        'name': "Stycast 2662 (10–60 GHz, 1.385 g/cc)",
        'section': 1, 
        'freq_range_ghz': (10, 60),
        'eps_params': {
            'B': 0.4099 + 0.0071j, 
            'C': 0.8644 - 0.0551j, 
            'D': 0.1859 - 0.085j, 
            'G': 0.8048 + 0.4175j, 
            'H': 0.0032 - 0.0182j, 
            'I': 0.0103 + 0.0093j, 
            'J': -0.0001 - 0.0002j}
    },
    { 
        'name': "Corning 7940 fused silica (2.201 g/cc, 10–100 GHz)",
        'section': 1, 
        'freq_range_ghz': (10, 100),
        'eps_params': {
            'B': 0.9389 - 0.0003j, 
            'C': 0.9413 - 0.0002j, 
            'D': 0.0261 + 0.0008j, 
            'G': 0.9381 - 0.0005j, 
            'H': 0.0017 + 0j, 
            'I': -0.0001 + 0.0026j, 
            'J': 0.000035 + 0.00000131j}
    },
    { 
        'name': "Corning 7957 fused silica (2.20 g/cc, 27–60 GHz)",
        'section': 1, 
        'freq_range_ghz': (27, 60),
        'eps_params': {
            'B': 0.9213 - 0.0307j, 
            'C': 0.936 - 0.0203j, 
            'D': 0.047 + 0.0524j, 
            'G': 0.9583 - 0.077j, 
            'H': 0.0001 + 0.0064j, 
            'I': -0.0064 + 0.0019j, 
            'J': 0.0000363 + 0.0000644j}
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
            'C': 7e-2+0.11j, 
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
        'name': "Silicon (2.33 g/cc) (9–12.4 GHz) (nominal εr = 10.2; Accumet Engineering)", 
        'section': 6, 
        'freq_range_ghz': (9, 12.4), 
        'eps_params': {
            'B': 3.89+0.008j, 
            'C': 3.89+0.008j, 
            'D': -0.002+0.002j, 
            'E': -0.002+0.002j, 
            'F': 3.89+0.008j, 
            'G': 440-1702j, 
            'H': -7627+10622j},
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
        'name': "Syntactic foam F6555 (0°)",
        'section': 7,
        'freq_range_ghz': (20, 100),
        'eps_params': {
            'B': 0.52 - 0.003j, 
            'C': 0.5 - 0.01j, 
            'D': -0.21 + 0.01j, 
            'G': 0.63 - 0.003j, 
            'H': 0.002 - 0.0003j, 
            'I': -0.003j, 
            'J': -0.00002 - 0.000004j}
    },
    {
        'name': "Syntactic foam F6555 (90°)",
        'section': 7,
        'freq_range_ghz': (20, 100),
        'eps_params': {
            'B': 0.63 + 0.004j, 
            'C': 0.75 + 0.02j, 
            'D': -0.14 - 0.01j, 
            'G': 0.6 - 0.0001j, 
            'H': 0.001 + 0.0j, 
            'I': 0.0004 - 0.002j, 
            'J': -0.00002 - 0.000004j}, 
    },
    {
        'name': "Honeycomb HRH-310 (0°)",
        'section': 7,
        'freq_range_ghz': (10, 60),
        'eps_params': {
            'B': 0.264 - 0.0004j, 
            'C': 0.266 - 0.0004j, 
            'D': -0.03 + 0.01j, 
            'G': 0.263 - 0.0007j, 
            'H': 0.002 + 0.0001j, 
            'I': -0.0008 - 0.003j, 
            'J': -0.00007 + 0.00001j}
    },
    {
        'name': "Honeycomb HRH-310 (90°)",
        'section': 7,
        'freq_range_ghz': (10, 60),
        'eps_params': {
            'B': 0.254 + 0.0002j,
            'C': 0.254 + 0.0002j,
            'D': 0.0002 + 0.0j,
            'G': 0.254 + 0.0002j,
            'H': -0.000002 + 0.0j,
            'I': -0.00002 - 0.0007j,
            'J': -0.00002 + 0.000001j
        }
    },
    {
        'name': "Honeycomb HRP 1/4-in cell (0°)",
        'section': 7,
        'freq_range_ghz': (30, 60),
        'eps_params': {
            'B': 0.331 + 0.045j,
            'C': 0.378 + 0.035j,
            'D': -0.111 + 0.09j,
            'G': 0.634 + 0.0002j,
            'H': 0.018 + 0.02j,
            'I': -0.02 + 0.005j,
            'J': 0.0001 + 0.0005j
        }
    },
    {
        'name': "Honeycomb HRP 1/4-in cell (90°)",
        'section': 7,
        'freq_range_ghz': (30, 60),
        'eps_params': {
            'B': 0.33 + 0.098j,
            'C': 0.193 + 0.04j,
            'D': 0.24 - 0.07j,
            'G': 0.012 - 0.015j,
            'H': 0.13 - 0.06j,
            'I': 0.0006 - 0.03j,
            'J': -0.0009 + 0.000009j
        }
    },
    {
        'name': "Honeycomb HRP 1/16-in cell (0°)",
        'section': 7,
        'freq_range_ghz': (30, 60),
        'eps_params': {
            'B': 0.297 + 0.004j,
            'C': 0.297 + 0.004j,
            'D': -0.001 + 0.002j,
            'G': 0.31 + 0.005j,
            'H': 0.007 + 0.0008j,
            'I': -0.003 + 0.009j,
            'J': 0.0002 + 0.0001j
        }
    },
    {
        'name': "Honeycomb HRP 1/16-in cell (90°)",
        'section': 7,
        'freq_range_ghz': (30, 60),
        'eps_params': {
            'B': 0.267 + 0.006j,
            'C': 0.267 + 0.006j,
            'D': 0.0004 + 0.0001j,
            'G': 0.267 + 0.006j,
            'H': 0.0004 + 0.0001j,
            'I': -0.0001 - 0.0009j,
            'J': -0.00004 - 0.000005j
        }
    },
    {
        'name': "Honeycomb HRH-78 (0°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.258 + 0.0007j,
            'C': 0.259 + 0.0007j,
            'D': 0.023 + 0.0007j,
            'G': 0.258 + 0.0006j,
            'H': -0.0013 - 0.0001j,
            'I': -0.0001 - 0.001j,
            'J': -0.000046 + 0.000002j
        }
    },
    {
        'name': "Honeycomb HRH-78 (90°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.27 - 0.0001j,
            'C': 0.27 - 0.0002j,
            'D': -0.006 + 0.0002j,
            'G': 0.27 - 0.0004j,
            'H': 0.001 - 0.0005j,
            'I': 0.0001 + 0.0015j,
            'J': 0.00006 - 0.000003j
        }
    },
    {
        'name': "Honeycomb HRH-10 (0°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.258 + 0.0007j,
            'C': 0.259 + 0.0007j,
            'D': 0.025 + 0.0007j,
            'G': 0.258 + 0.0006j,
            'H': -0.0013 - 0.0001j,
            'I': -0.0001 - 0.001j,
            'J': -0.00005 + 0.000002j
        }
    },
    {
        'name': "Honeycomb HRH-10 (90°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.253 + 0.0003j,
            'C': 0.255 + 0.0003j,
            'D': 0.029 + 0.0004j,
            'G': 0.251 + 0.0003j,
            'H': -0.0015 - 0.00002j,
            'I': -0.0005 - 0.0005j,
            'J': -0.00004 + 0.0000003j
        }
    },
    {
        'name': "Honeycomb para-aramid (0°)",
        'section': 7,
        'freq_range_ghz': (5, 40),
        'eps_params': {
            'B': 0.266 + 0.0006j,
            'C': 0.266 + 0.0006j,
            'D': 0.002 + 0.0j,
            'G': 0.267 + 0.0006j,
            'H': 0.0004 + 0.002j,
            'I': 0.0001 + 0.0j,
            'J': 0.0001 + 0.0j
        }
    },
    {
        'name': "Honeycomb para-aramid (90°)",
        'section': 7,
        'freq_range_ghz': (5, 40),
        'eps_params': {
            'B': 0.262 + 0.0004j,
            'C': 0.263 + 0.0004j,
            'D': -0.017 + 0.0j,
            'G': 0.262 + 0.0004j,
            'H': -0.0005 - 0.002j,
            'I': -0.00003 + 0.0j,
            'J': -0.00003 + 0.0j
        }
    },
    {
        'name': "Honeycomb HRH-327 (0°)",
        'section': 7,
        'freq_range_ghz': (30, 60),
        'eps_params': {
            'B': 0.267 + 0.006j,
            'C': 0.267 + 0.006j,
            'D': 0.0004 + 0.0001j,
            'G': 0.267 + 0.006j,
            'H': 0.0004 - 0.0001j,
            'I': -0.0001 - 0.0009j,
            'J': -0.00004 + 0.000004j
        }
    },
    {
        'name': "Honeycomb HRH-327 (90°)",
        'section': 7,
        'freq_range_ghz': (30, 60),
        'eps_params': {
            'B': 0.297 + 0.005j,
            'C': 0.297 + 0.005j,
            'D': -0.001 + 0.002j,
            'G': 0.31 + 0.005j,
            'H': 0.007 + 0.0008j,
            'I': -0.003 + 0.009j,
            'J': 0.0002 + 0.0001j
        }
    },
    {
        'name': "Honeycomb ES PEI-E-glass (0°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.253 - 0.001j,
            'C': 0.257 - 0.0007j,
            'D': 0.042 + 0.011j,
            'G': 0.254 - 0.002j,
            'H': -0.002 - 0.001j,
            'I': -0.002 + 0.0007j,
            'J': 0.0000008 + 0.00003j
        }
    },
    {
        'name': "Honeycomb ES PEI-E-glass (90°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.271 - 0.0002j,
            'C': 0.271 - 0.0002j,
            'D': -0.007 - 0.002j,
            'G': 0.272 + 0.0001j,
            'H': -0.003 + 0.002j,
            'I': 0.0002 - 0.004j,
            'J': -0.0001 + 0.0j
        }
    },
    {
        'name': "PBI Honeycomb (0° incidence)",
        'section': 7,
        'freq_range_ghz': (4, 100),
        'eps_params': {
            'B': 0.286 + 0.002j,
            'C': 0.288 + 0.002j,
            'D': -0.04 - 0.008j,
            'G': 0.292 + 0.002j,
            'H': -0.003 - 0.0002j,
            'I': 0.0005 - 0.003j,
            'J': -0.000009 - 0.000003j
        }
    },
    {
        'name': "PBI Honeycomb (20° incidence)",
        'section': 7,
        'freq_range_ghz': (70, 100),
        'eps_params': {
            'B': 0.41 - 0.12j,
            'C': 0.4 - 0.25j,
            'D': -0.14 - 0.14j,
            'G': 0.297 - 0.07j,
            'H': 0.008 - 0.006j,
            'I': 0.003 - 0.01j,
            'J': -0.0001 - 0.00004j
        }
    },
    {
        'name': "PBI Honeycomb (40° incidence)",
        'section': 7,
        'freq_range_ghz': (70, 100),
        'eps_params': {
            'B': 0.52 - 0.03j,
            'C': 0.54 - 0.02j,
            'D': 0.083 + 0.019j,
            'G': 0.462 + 0.05j,
            'H': 0.08 + 0.004j,
            'I': 0.03 - 0.07j,
            'J': -0.002 - 0.0008j
        }
    },
    {
        'name': "PBI Honeycomb (60° incidence)",
        'section': 7,
        'freq_range_ghz': (70, 100),
        'eps_params': {
            'B': 0.32 - 0.01j,
            'C': 0.32 - 0.01j,
            'D': -0.03 - 0.01j,
            'G': 0.35 + 0.003j,
            'H': -0.002 - 0.003j,
            'I': 0.002 - 0.001j,
            'J': 0.00002 - 0.00003j
        }
    },
    {
        'name': "Honeycomb polycarbonate 1/8-in (0°)",
        'section': 7,
        'freq_range_ghz': (8, 26),
        'eps_params': {
            'B': 0.293 + 0.0003j,
            'C': 0.293 + 0.0003j,
            'D': 0.008 - 0.002j,
            'G': 0.294 + 0.0003j,
            'H': -0.0014 - 0.0012j,
            'I': 0.0005 + 0.003j,
            'J': 0.00006 + 0.00001j
        }
    },
    {
        'name': "Honeycomb polycarbonate 1/8-in (90°)",
        'section': 7,
        'freq_range_ghz': (8, 26),
        'eps_params': {
            'B': 0.304 - 0.005j,
            'C': 0.31 - 0.005j,
            'D': -0.05 + 0.02j,
            'G': 0.303 - 0.004j,
            'H': 0.002 - 0.0008j,
            'I': -0.0004 - 0.003j,
            'J': -0.00005 + 0.000006j
        }
    },
    {
        'name': "Honeycomb polyimide 1/4-in (0°)",
        'section': 7,
        'freq_range_ghz': (18, 45),
        'eps_params': {
            'B': 0.288 + 0.0j,
            'C': 0.288 + 0.0j,
            'D': -0.0004 + 0.0j,
            'G': 0.287 - 0.0002j,
            'H': 0.0004 - 0.00003j,
            'I': 0.0002 + 0.005j,
            'J': 0.0002 - 0.000002j
        }
    },
    {
        'name': "Polyurethane foam 10 lb/ft3 (0°)",
        'section': 7,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.293 - 0.0002j,
            'C': 0.293 - 0.0002j,
            'D': 0.007 + 0.002j,
            'G': 0.291 - 0.0001j,
            'H': -0.0003 - 0.0001j,
            'I': 0.00002 - 0.0005j,
            'J': -0.00001 + 0.0000009j
        }
    },
    {
        'name': "Polyurethane foam 6 lb/ft3 (0°)",
        'section': 7,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.278 + 0.0004j,
            'C': 0.278 + 0.0004j,
            'D': 0.0001 - 0.0001j,
            'G': 0.278 + 0.0004j,
            'H': 0.0000005 - 0.0000002j,
            'I': 0.00005 + 0.0002j,
            'J': 0.000003 - 0.0000006j
        }
    },
    {
        'name': "Carbon reticulated foam Sample C",
        'section': 7,
        'freq_range_ghz': (0.5, 6),
        'eps_params': {
            'B': 1.55 + 0.28j,
            'C': -0.64 + 1.81j,
            'D': -0.95 + 0.16j,
            'G': 0.93 + 0.86j,
            'H': 0.5 + 0.46j,
            'I': -0.41 - 0.11j,
            'J': -0.14 - 0.005j
        }
    },
    {
        'name': "Carbon reticulated foam Sample B",
        'section': 7,
        'freq_range_ghz': (0.5, 6),
        'eps_params': {
            'B': 1.59 + 0.39j,
            'C': -0.43 + 1.61j,
            'D': -1.1 + 0.47j,
            'G': -0.5 + 1.44j,
            'H': 0.31 - 0.12j,
            'I': -0.46 - 0.11j,
            'J': -0.11 + 0.05j
        }
    },
    {
        'name': "Carbon reticulated foam Sample A",
        'section': 7,
        'freq_range_ghz': (0.5, 6),
        'eps_params': {
            'B': 1.28 - 0.55j,
            'C': -0.32 + 2.61j,
            'D': -0.84 + 0.11j,
            'G': 1.55 + 0.44j,
            'H': -0.06 + 0.31j,
            'I': -0.44 + 0.17j,
            'J': -0.04 + 0.15j
        }
    },
    {
        'name': "110 Polymethacrylimide-1 foam (0°)",
        'section': 7,
        'freq_range_ghz': (1, 100),
        'eps_params': {
            'B': 0.292 + 0.002j,
            'C': 0.292 + 0.002j,
            'D': 0.0 + 0.0j,
            'G': 0.292 + 0.002j,
            'H': 0.0 + 0.0j,
            'I': 0.0 + 0.0j,
            'J': 0.0 + 0.0j
        }
    },
    {
        'name': "110 Polymethacrylimide-2 foam (0°)",
        'section': 7,
        'freq_range_ghz': (1, 100),
        'eps_params': {
            'B': 0.321 - 0.003j,
            'C': 0.365 - 0.003j,
            'D': -0.12 + 0.014j,
            'G': 0.318 - 0.004j,
            'H': -0.001 + 0.002j,
            'I': -0.0003 - 0.002j,
            'J': -0.00002 + 0.000004j
        }
    },
    {
        'name': "200 Polymethacrylimide foam (0°)",
        'section': 7,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.322 + 0.003j,
            'C': 0.322 + 0.003j,
            'D': 0.0007 + 0.002j,
            'G': 0.322 + 0.003j,
            'H': 0.0001 + 0.0001j,
            'I': -0.0005 + 0.0008j,
            'J': 0.00002 + 0.000008j
        }
    },
    {
        'name': "300 Polymethacrylimide foam (0°)",
        'section': 7,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.273 + 0.007j,
            'C': 0.313 + 0.005j,
            'D': 0.12 - 0.001j,
            'G': 0.161 - 0.008j,
            'H': 0.033 + 0.002j,
            'I': -0.03 - 0.002j,
            'J': 0.0
        }
    },
    {
        'name': "51 Polymethacrylimide foam (0°)",
        'section': 7,
        'freq_range_ghz': (8, 26),
        'eps_params': {
            'B': 0.289 - 0.002j,
            'C': 0.305 - 0.002j,
            'D': -0.082 + 0.007j,
            'G': 0.287 - 0.002j,
            'H': -0.001 + 0.0003j,
            'I': -0.0001 - 0.002j,
            'J': -0.00002 + 0.000001j
        }
    },
    {
        'name': "71 Polymethacrylimide foam (0°)",
        'section': 7,
        'freq_range_ghz': (9, 17),
        'eps_params': {
            'B': 0.2753 + 0.0017j,
            'C': 0.2753 + 0.0017j,
            'D': 0.002 + 0.0004j,
            'G': 0.2754 + 0.0017j,
            'H': 0.0038 + 0.001j,
            'I': -0.0012 + 0.0041j,
            'J': -0.0004 + 0.0001j
        }
    },
    {
        'name': "31 Polymethacrylimide foam (0°)",
        'section': 7,
        'freq_range_ghz': (8, 26),
        'eps_params': {
            'B': 0.2625 + 0.0002j,
            'C': 0.2625 + 0.0002j,
            'D': -0.0005 + 0.0j,
            'G': 0.2625 + 0.0002j,
            'H': 0.0 + 0.0003j,
            'I': 0.0001 + 0.0j,
            'J': 0.0 + 0.0j
        }
    },
    {
        'name': "Polystyrene foam 7.8 lb/ft3",
        'section': 7,
        'freq_range_ghz': (9, 18),
        'eps_params': {
            'B': 0.2974 + 0.0003j,
            'C': 0.6337 + 0.0002j,
            'D': 0.0 + 0.0j,
            'G': 0.3404 + 0.0002j,
            'H': 0.1091 + 0.0004j,
            'I': 0.0428 + 0.0428j,
            'J': -0.0026 + 0.0j
        }
    },
    {
        'name': "Polystyrene foam 12.1 lb/ft3",
        'section': 7,
        'freq_range_ghz': (9, 18),
        'eps_params': {
            'B': 0.2959 + 0.0015j,
            'C': 0.2959 + 0.0015j,
            'D': 0.0012 + 0.0005j,
            'G': 0.2964 + 0.0015j,
            'H': -0.0019 + 0.0011j,
            'I': -0.001 + 0.005j,
            'J': -0.0002 + 0.0001j
        }
    },
    {
        'name': "Polystyrene foam 13.9 lb/ft3",
        'section': 7,
        'freq_range_ghz': (9, 18),
        'eps_params': {
            'B': 0.2457 + 0.0001j,
            'C': 0.2923 + 0.0001j,
            'D': 0.1776 + 0.0001j,
            'G': 0.035 + 0.0001j,
            'H': 0.084 + 0.0001j,
            'I': -0.00862 + 0.0j,
            'J': -0.0092 + 0.0j
        }
    },
    {
        'name': "Polystyrene foam 15.7 lb/ft3",
        'section': 7,
        'freq_range_ghz': (9, 18),
        'eps_params': {
            'B': 0.2454 + 0.0001j,
            'C': 0.2883 + 0.0001j,
            'D': 0.1733 + 0.0j,
            'G': 0.03331 + 0.0j,
            'H': 0.0868 + 0.0001j,
            'I': 0.0 + 0.0j,
            'J': 0.0 + 0.0j
        }
    },
    {
        'name': "Polystyrene foam 17.0 lb/ft3",
        'section': 7,
        'freq_range_ghz': (9, 18),
        'eps_params': {
            'B': 0.3977 + 0.0001j,
            'C': 0.8283 + 0.0005j,
            'D': 0.0 + 0.0j,
            'G': 0.3271 + 0.0003j,
            'H': 0.0302 + 0.0002j,
            'I': 0.0347 + 0.0001j,
            'J': -0.0033 + 0.0j
        }
    },
    {
        'name': "Polystyrene foam 20.0 lb/ft3",
        'section': 7,
        'freq_range_ghz': (9, 18),
        'eps_params': {
            'B': 0.3381 + 0.0005j,
            'C': 0.3382 + 0.0005j,
            'D': 0.0053 + 0.0002j,
            'G': 0.3386 + 0.0005j,
            'H': 0.0073 - 0.0001j,
            'I': -0.0008 + 0.0j,
            'J': 0.0 + 0.0j
        }
    },
    {
        'name': "Bismaleimide BMI F650, 1.27 g/cc (18–60 GHz)",
        'section': 8,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.5471+0.0387j,
            'C': 0.6184+0.0324j,
            'D': 0.1048-0.0071j,
            'G': 1.7022-0.0433j,
            'H': 0.0153+0.0022j,
            'I': -0.0015+0.0162j,
            'J': 0.0002
        }
    },
    {
        'name': "Bismaleimide BMI F650, 1.27 g/cc (18–100 GHz)",
        'section': 8,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.7982+0.0217j,
            'C': 0.7982+0.0217j,
            'D': 0.0054+0.0038j,
            'G': 0.7987+0.0216j,
            'H': 0.0005+0.0005j,
            'I': -0.0019+0.0026j,
            'J': 5.91E-005+2.91E-005j
        }
    },
    {
        'name': "Celazole polybenzamidazole PBI (75–100 GHz), 1.3 g/cc",
        'section': 8,
        'freq_range_ghz': (75, 100),
        'eps_params': {
            'B': 0.6934+0.1502j,
            'C': 0.6812+0.3522j,
            'D': -0.1589+0.0196j,
            'G': 0.6014-0.0045j,
            'H': 0.0046+0.0067j,
            'I': -0.001-0.0078j,
            'J': -0.0001
        }
    },
    {
        'name': "Cyanate ester 561, (20–60 GHz), 1.22 g/cc",
        'section': 8,
        'freq_range_ghz': (20, 60),
        'eps_params': {
            'B': 0.707+0.0013j,
            'C': 0.707+0.0013j,
            'D': 0.004-0.0009j,
            'G': 0.7075+0.0011j,
            'H': 0.0007-0.0002j,
            'I': 0.0009+0.0038j,
            'J': 0.0001
        }
    },
    {
        'name': "Cyanate ester-2 (30–100 GHz), 1.22 g/cc",
        'section': 8,
        'freq_range_ghz': (30, 100),
        'eps_params': {
            'B': 0.6469+0.0546j,
            'C': 0.6796+0.0416j,
            'D': 0.0881-0.0167j,
            'G': 0.4457+0.0811j,
            'H': 0.0106-0.0055j,
            'I': -0.0034-0.0122j,
            'J': -0.0006
        }
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
        'name': "Polyester F141 (18–60 GHz), 1.38 g/cc",
        'section': 8,
        'freq_range_ghz': (18, 60),
        'eps_params': {
            'B': 0.7543+0.0325j,
            'C': 0.7538+0.0323j,
            'D': 0.0011+0.0047j,
            'G': 0.7653+0.0351j,
            'H': 0.0071+0.0035j,
            'I': -0.0063+0.0066j,
            'J': 0.0002+0.0002j
        }
    },
    {
        'name': "Epoxy F161, 1.243 g/cc (18–100 GHz)",
        'section': 8,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.8804+0.0221j,
            'C': 0.9002+0.0234j,
            'D': -0.0688-0.0124j,
            'G': 0.8758+0.0213j,
            'H': -0.0006+0.0007j,
            'I': -0.0015j,
            'J': -1.12E-005+1.61E-007j
        }
    },
    {
        'name': "2555 Meltbond adhesive (20–60 GHz)",
        'section': 8,
        'freq_range_ghz': (20, 60),
        'eps_params': {
            'B': 0.7346+0.0041j,
            'C': 0.7345+0.0041j,
            'D': 0.0012+0.0001j,
            'G': 0.7355+0.0041j,
            'H': 0.0004,
            'I': -0.0002+0.0035j,
            'J': 9.70E-005+5.53E-006j
        }
    },
    {
        'name': "Plexiglass acrylic (PMMA), 1.2 g/cc (26–100 GHz)",
        'section': 8,
        'freq_range_ghz': (26, 100),
        'eps_params': {
            'B': 0.6719+0.002j,
            'C': 0.6724+0.002j,
            'D': 0.0185+0.0006j,
            'G': 0.6692+0.002j,
            'H': 0.0052+0.0001j,
            'I': -0.0001+0.006j,
            'J': 8.54E-005+2.25E-006j
        }
    },
    {
        'name': "Polyester, F148 (18–100 GHz), ~1.4 g/cc",
        'section': 8,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.9813+0.0828j,
            'C': 0.931-0.0515j,
            'D': 0.0068+0.0273j,
            'G': 0.007+0.0175j,
            'H': 0.0356-0.007j,
            'I': -0.0024-0.0289j,
            'J': -0.0009+0.0001j
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
        'name': "Polyimide bismaleimide F178 (18–100 GHz), 1.297 g/cc",
        'section': 8,
        'freq_range_ghz': (18, 100),
        'eps_params': {
            'B': 0.504-0.0424j,
            'C': 0.5854-0.0411j,
            'D': 0.1004+0.0055j,
            'G': 1.6253+0.1025j,
            'H': 0.0086-0.0017j,
            'I': 0.0021+0.0096j,
            'J': 9.82E-005-1.99E-005j
        }
    },
    {
        'name': "Polyethylene (8–40 GHz), 0.93–0.94 g/cc",
        'section': 8,
        'freq_range_ghz': (8, 40),
        'eps_params': {
            'B': 0.6329+0.0007j,
            'C': 1.0517-0.0021j,
            'D': -0.2925-0.0002j,
            'G': 0.5377+0.003j,
            'H': -0.0022+0.0007j,
            'I': -0.0001-0.0111j,
            'J': -2.67E-004+2.19E-006j
        }
    },
    {
        'name': "Polytetrafluoroethylene (PTFE) (10–100 GHz), 2.13–2.19 g/cc",
        'section': 8,
        'freq_range_ghz': (10, 100),
        'eps_params': {
            'B': 0.5635+0.0002j,
            'C': 0.6481+0.0006j,
            'D': -0.1309+0.0001j,
            'G': 0.5095-0.0007j,
            'H': 0.0009+0.0002j,
            'I': -0.0034j,
            'J': -3.40E-005+1.74E-007j
        }
    },
    {
        'name': "Polyamide 7 (10–16 GHz avg.), 1.15–1.25 g/cc",
        'section': 8,
        'freq_range_ghz': (10, 16),
        'eps_params': {
            'B': 3.1+0.003j
        }
    },
    {
        # Was missing E & F columns so I (Glazer) added them
        'name': "7058 Epoxy w/ ~40% vol silica hollow spheres (2–18 GHz)",
        'section': 8,
        'freq_range_ghz': (2, 18),
        'eps_params': {
            'B': 0.7275+0.0758j,
            'C': 2.4321+0.1323j,
            'D': -3.8007-0.9919j, 
            'E': 1.6216+0.2312j, #This was 'G' before but it actually contains values from 'E' --> it kept the same BCDGHIJ pattern but this epoxy has BCDEFGHIJ so it just missed 'I' and 'J' values and skipped the column labels for 'E' and 'F'
            'F': -3.3603+1.9301j, # Also used to be 'H' but contains values from 'F' 
            'G': 0.9885-0.0586j, 
            'H': -9E-003+0.0107j,
            'I': -2E-004-2.3E-003j, #Added manually
            'J': -1.62E-004+1.21E-005j #Added manually
        }
    }
]