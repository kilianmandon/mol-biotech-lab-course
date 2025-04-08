import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Set seaborn style
# sns.set(style="whitegrid")

# Calibration data (concentrations and absorbances)
concentrations_bsa = np.array([10, 20, 50, 100, 200, 400])
absorbances_bsa = np.array([0.008774988, 0.021975003, 0.067174993, 0.123975016, 0.238475002, 0.476574995])

# Protein data for PelB and nonPelB (blanked absorbances)
pelb_absorbances = np.array([0.158225007, 0.067625009, 0.02327501, 7.5005E-05, -0.008075006, -0.013025008,
                             -0.001775004, -0.002925001, -0.001924999])

nonpelb_absorbances = np.array([0.175475009, 0.056874998, 0.023125, 0.026125006, 0.009075008, 0.001174994,
                                0.001274996, -0.003575005, 0.001425005])

# Concentration factors for each measurement
concentration_factors = np.array([2, 5, 10, 2, 5, 10, 2, 5, 10])

# Step 1: Perform linear regression to find the equation of the calibration curve
slope, intercept, r_value, p_value, std_err = linregress(concentrations_bsa, absorbances_bsa)

# Print regression results
print("Calibration Linear Regression Results:")
print(f"Slope: {slope:.6f}")
print(f"Intercept: {intercept:.6f}")
print(f"R-squared: {r_value**2:.6f}")
print(f"P-value: {p_value:.6f}")
print(f"Standard Error: {std_err:.6f}")

# Step 2: Calculate concentrations from absorbances for PelB and nonPelB
def calculate_concentration(absorbances, slope, intercept):
    return (absorbances - intercept) / slope

pelb_concentrations = calculate_concentration(pelb_absorbances, slope, intercept)
nonpelb_concentrations = calculate_concentration(nonpelb_absorbances, slope, intercept)

# Print calculated concentrations for PelB and nonPelB
print("\nCalculated Concentrations for PelB (in µg/mL):")
print(pelb_concentrations)

print("\nCalculated Concentrations for NonPelB (in µg/mL):")
print(nonpelb_concentrations)

# Step 3: Multiply by concentration factors to get adjusted concentrations
pelb_adjusted_concentrations = pelb_concentrations * concentration_factors
nonpelb_adjusted_concentrations = nonpelb_concentrations * concentration_factors

# Print adjusted concentrations
print("\nAdjusted Concentrations for PelB (in µg/mL):")
print(pelb_adjusted_concentrations)

print("\nAdjusted Concentrations for NonPelB (in µg/mL):")
print(nonpelb_adjusted_concentrations)

# Step 4: Split data into blocks of 3
def split_into_blocks(concentrations):
    return [concentrations[i:i+3] for i in range(0, len(concentrations), 3)]

pelb_blocks = split_into_blocks(pelb_adjusted_concentrations)
nonpelb_blocks = split_into_blocks(nonpelb_adjusted_concentrations)

# Print split blocks
print("\nPelB Adjusted Concentrations (split into blocks of 3):")
for i, block in enumerate(pelb_blocks, 1):
    print(f"Block {i}: {block}")

print("\nNonPelB Adjusted Concentrations (split into blocks of 3):")
for i, block in enumerate(nonpelb_blocks, 1):
    print(f"Block {i}: {block}")

# Step 5: Calculate mean and standard deviation for each block
def calculate_block_stats(blocks):
    means = [np.mean(block[:-1]) for block in blocks]
    std_devs = [np.std(block[:-1]) for block in blocks]
    return means, std_devs

pelb_means, pelb_std_devs = calculate_block_stats(pelb_blocks)
nonpelb_means, nonpelb_std_devs = calculate_block_stats(nonpelb_blocks)

# Print means and std devs
print("\nPelB Mean and Standard Deviation per Block:")
for i in range(3):
    print(f"Block {i+1}: Mean = {pelb_means[i]:.3f}, Std Dev = {pelb_std_devs[i]:.3f}")

print("\nNonPelB Mean and Standard Deviation per Block:")
for i in range(3):
    print(f"Block {i+1}: Mean = {nonpelb_means[i]:.3f}, Std Dev = {nonpelb_std_devs[i]:.3f}")

# Step 6: Plot the regression (Concentrations on x-axis and Absorbances on y-axis)
plt.figure(figsize=(8, 6))
plt.scatter(concentrations_bsa, absorbances_bsa, color="blue", label="Calibration Data")
plt.plot(concentrations_bsa, slope * concentrations_bsa + intercept, color="red", label="Linear Fit")
plt.xlabel("Concentration (µg/mL)")
plt.ylabel("Blanked Absorbance (-)")
plt.legend()
plt.tight_layout()
plt.show()