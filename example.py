from PIC_calculator import *
import pandas as pd

example_file = pd.read_csv("example_data.csv")
freqs = compute_population_PIC(example_file, diploid=True)
print(freqs)