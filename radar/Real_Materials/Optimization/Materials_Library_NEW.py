materials_data = [
    { 
        'name': "Fused silica glass (Dynasil 4000, 2.16–2.2 g/cc) (0.1–100 GHz)", #5
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
        'name': "80 µm 9%/vol in epoxy, 1.38 g/cc", #7
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
        'name': "80 µm 16%/vol in epoxy, 1.6 g/cc", #8
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
        'name': "80 µm 16.7%/vol in epoxy, 1.68 g/cc", #9
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
        'name': "80 µm 41.1%/vol in epoxy, 2.68 g/cc", #12
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
        'name': "80 µm 49.4%/vol in epoxy, ~3.0 g/cc", #13
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
        'name': "80 µm 61.4%/vol in epoxy, ~3.52 g/cc", #16
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
        'name': "80 µm 61.8%/vol in epoxy, ~3.53 g/cc", #17
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
        'name': "80 µm 76.1%/vol in epoxy, ~4.12 g/cc", #18
        'section': 4,
        'freq_range_ghz': (0.001, 10),
        'chi_m_params': {
            'B': 14.20, 
            'C': 0.18, 
            'D': 0.053},
        'eps1_params': {
            'B': 3.31+.11j, 
            'C': 2.32+0.15j, 
            'D': 5e-3-6e-3j, 
            'E': 1.87-.22j, 
            'F': 12.1-.76j, 
            'G': -2.2-19.8j
        },
        'eps2_params': {
            'B': 3.93+2e-2j, 
            'C': .97-.13j, 
            'D': 3e2+.15j, 
            'E': -.26+.32j, 
            'F': 2.8+.16j, 
            'G': 13.1-2.91j, 
            'H': -11.8-19j
        }
    },
    {
        'name': "500-nm Fe 7% + 80-µm Ferrite 7%/vol in epoxy, 1.8 g/cc", #19
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
        'name': "500-nm Fe 10.2% + 80-µm Ferrite 10.1%/vol in epoxy, 2.1 g/cc", #20
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
        'name': "500-nm Fe 13.4% + 80-µm Ferrite 13.6%/vol in epoxy, 2.43 g/cc", #21
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
        'name': "500-nm Fe 23.3% + 80-µm Ferrite 23.3%/vol in epoxy, 3.4 g/cc", #24
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
]