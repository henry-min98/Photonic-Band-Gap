import sys
import flow

import math
import subprocess
#import numpy as np
import meep as mp
from meep import mpb
from IPython.utils.capture import capture_output
from tqdm.auto import tqdm
import time
import matplotlib.pyplot as plt
import re
import pandas as pd

class MyProject(flow.FlowProject):
    pass

sqrt_half = math.sqrt(0.5)
geometry_lattice = mp.Lattice(
    basis_size=mp.Vector3(sqrt_half, sqrt_half, sqrt_half),
    basis1=mp.Vector3(0, 1, 1),
    basis2=mp.Vector3(1, 0, 1),
    basis3=mp.Vector3(1, 1,)
)

# Corners of the irreducible Brillouin zone for the fcc lattice,
# in a canonical order:
vlist = [
    mp.Vector3(0, 0.5, 0.5),        # X
    mp.Vector3(0, 0.625, 0.375),    # U
    mp.Vector3(0, 0.5, 0),          # L
    mp.Vector3(0, 0, 0),            # Gamma
    mp.Vector3(0, 0.5, 0.5),        # X
    mp.Vector3(0.25, 0.75, 0.5),    # W
    mp.Vector3(0.375, 0.75, 0.375)  # K
]

resolution = 16  # use a 16x16x16 grid
mesh_size = 5
num_bands = 5

k_points = mp.interpolate(4, vlist)

@MyProject.operation
@MyProject.post(lambda job: 'gaps' in job.document)
def get_band_structure(job):
    diel = mp.Medium(epsilon=job.sp.epsilon)
    geometry = [mp.Sphere(job.sp.r, center=mp.Vector3(0.125, 0.125, 0.125), material=diel),
                mp.Sphere(job.sp.r, center=mp.Vector3(-0.125, -0.125, -0.125), material=diel)]

    with job:
        ms = mpb.ModeSolver(
            geometry_lattice=geometry_lattice,
            k_points=k_points,
            geometry=geometry,
            resolution=resolution,
            num_bands=num_bands,
            mesh_size=mesh_size
        )
        ms.run()
        job.document['freqs'] = ms.all_freqs
        job.document['gaps'] = ms.gap_list


if __name__ == "__main__":
    MyProject().main()
