import signac
import numpy as np

project=signac.init_project(name='photonics', root='./')

R = list(sorted(set([*np.arange(0.2, 0.35, 0.01, dtype=float), *np.arange(0.05, 0.5, 0.05, dtype=float)])))
eps = np.arange(4, 17, 1, dtype=int)
input((R, eps))

for r in R:
	for e in eps:
		job = project.open_job({"r": round(r,3), "epsilon": round(e)}).init()
