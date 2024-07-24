import pandas as pd

def compute_frequencies(df, diploid=True):
    if diploid:
        prefixes = set([col[:-1] for col in df.columns if col not in ['ID', 'Pop']])
        frequency_counts = {}

        for prefix in prefixes:
            cols = [col for col in df.columns if col.startswith(prefix)]
            combined_values = df[cols].values.flatten()
            value_counts = pd.Series(combined_values).value_counts()
            if 0 in value_counts:
                value_counts = value_counts.drop(0)
            total_counts = value_counts.sum()
            frequency_counts[prefix] = value_counts / total_counts
        
        return frequency_counts
    
    else: 
        raise Exception("NOT IMPLEMENTED")
    
def split_populations(df, diploid=True):
    pops = df.Pop.unique()

    pop_freqs = {}

    for pop in pops:
        pop_freqs[pop] = compute_frequencies(df[df.Pop == pop], diploid=diploid)

    return pop_freqs

def compute_population_PIC(df, diploid=True, save=True, path="."):
    frequency_counts = split_populations(df, diploid=diploid)
    PICs = {}

    for population, loci in frequency_counts.items():
        PICs[population] = {}
        PIC_sum = 0
        for locus, frequencies in loci.items():
            sum_of_squares = (frequencies ** 2).sum()
            PIC = 1 - sum_of_squares - sum_of_squares**2 + (frequencies ** 4).sum()
            PIC = round(PIC, 2)
            PICs[population][locus] = PIC
            PIC_sum += PIC
        PICs[population]["mean"] = round(PIC_sum/len(loci), 2)
    
    PICs = pd.DataFrame(PICs)
    
    if save:
        PICs.to_excel(f"{path.strip('/')}/PIC_table.xlsx")

    return PICs


