import signac
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
df = pd.DataFrame(columns=['radius', 'epsilon', 'feature3','feature4'])


for job in tqdm(signac.get_project().find_jobs(doc_filter={"freqs.$exists": True})):
    #file.to_csv("gfg2.csv", header=headerList, index=False)
    row = [job.sp.r, job.sp.epsilon, max(np.array(job.document.freqs)[:, 1]), min(np.array(job.document.freqs)[:, 2])]
    df.loc[len(df)] = row
df.to_csv('gen_photonics_data.csv',index=False)

