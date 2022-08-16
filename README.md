# Selecting an Analog Sample
A code that allows for selection of an anlog sample in various parameter spaces. Adapted from Cat Fielder.

# Installation
Directly from Repository
```
git clone https://github.com/toribonidie/analog_stars
```

# Usage
This code has been adapted from Cat Fielder, who used it to select a Milky Way anlog sample. Her version can be found here: ```https://github.com/cfielder/MW_Morphology```

This code is sepcifically built to work around a cleaned sample. For example, in Bonidie et al. (2022), we selected both samples from stars in APOGEE DR16 that have passed the combined quality cuts from Hayes et al. (2020) and Mazzola et al. (2020). Further, to ensure that the presence of MW stars with very high S/N spectra does not introduce unwanted biases in our measurements, we required that the S/N of the stellar analogs be in the same range as the Sgr dSph members.

If you want to work with this specific sample please contact me!

# Description of Scripts
To make a sample of analogs, values are randomly drawn from the fiducial MW PDF in the parameter space of interest (minimum of two parameters). For each set of values, the nearest neighbors are found in a binary tree constructed from the volume-limited sample.

### Step 1:
Create a dataframe of your test sample (the sample you're interested in) and your training sample (the sample from which you want to select analogs). Make sure the parameters you want to match these dataframes on have the same names in both dataframes. In Bonidie et al. (2022), we used effective temperature, log(g) and [Fe/H] as the selection parameters.

### Step 2:
Create a "stats" dataframe that consists of the mean and standard deviation of each parameter in your test sample.

### Step 3: 
Run ```select_analogs.py```. The ```select_analogs()``` function takes in a dataframe of the test sample (the Sgr Dsph sample in Bonidie et al. (2022)) and a dataframe of the training sample (the MW star sample in Bonidie et al. (2022)), as well as the stats dataframe you create in step 2. Ensure the columns of each parameter of interest has the same name in each of these dataframes, This function accesses ```analog_auto.py```, which contains a function for selecting a single analog from the binary tree.
