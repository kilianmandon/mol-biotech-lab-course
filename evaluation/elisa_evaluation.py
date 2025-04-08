import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Set seaborn style
# sns.set(style="whitegrid")

# Calibration data (concentrations and absorbances in ng/mL and absorbance respectively)
concentrations_cal_b = np.array([100, 200, 500, 1000])  # Concentrations in ng/mL
absorbances_cal_b = np.array([0.284149997, 0.61900001, 2.511550091, 3.587449931])  # Absorbances

# New protein data for mCherry and PelB-mCherry (absorbances)
mcherry_absorbances = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 3.651999973, 2.459049962, 1.058100007])

pelb_mcherry_absorbances = np.array([3.15145006, 2.162149929, 1.213950001, 0.44455, 0.102749996, -0.016200006, 
                                     -0.067249998, -0.067400005, 0.0361])

# Step 1: Perform linear regression to find the equation of the calibration curve
slope, intercept, r_value, p_value, std_err = linregress(concentrations_cal_b, absorbances_cal_b)

# Print regression results
print("Calibration Linear Regression Results:")
print(f"Slope: {slope:.6f}")
print(f"Intercept: {intercept:.6f}")
print(f"R-squared: {r_value**2:.6f}")
print(f"P-value: {p_value:.6f}")
print(f"Standard Error: {std_err:.6f}")

# Step 2: Calculate concentrations from absorbances for mCherry and PelB-mCherry
def calculate_concentration(absorbances, slope, intercept):
    # Ignore NaN values by using np.nanmean to prevent crashes
    # valid_absorbances = absorbances[~np.isnan(absorbances)]
    valid_absorbances = absorbances
    return (valid_absorbances - intercept) / slope

mcherry_concentrations = calculate_concentration(mcherry_absorbances, slope, intercept)
pelb_mcherry_concentrations = calculate_concentration(pelb_mcherry_absorbances, slope, intercept)

# Print calculated concentrations for mCherry and PelB-mCherry
print("\nCalculated Concentrations for mCherry (in ng/mL):")
print(mcherry_concentrations)

print("\nCalculated Concentrations for PelB-mCherry (in ng/mL):")
print(pelb_mcherry_concentrations)

# Step 3: Plot the regression (Concentrations on x-axis and Absorbances on y-axis)
plt.figure(figsize=(8, 6))
plt.scatter(concentrations_cal_b, absorbances_cal_b, color="blue", label="Calibration Data")
plt.plot(concentrations_cal_b, slope * concentrations_cal_b + intercept, color="red", label="Linear Fit")
plt.xlabel("Concentration (ng/mL)")
plt.ylabel("Blanked Absorbance (-)")
plt.legend()
plt.tight_layout()
plt.show()

dilution = np.array([5, 10, 20, 5, 10, 20, 5, 10, 20])

# Optional: If you want to show the final concentrations of mCherry and PelB-mCherry
print("\nFinal Concentrations for mCherry (in µg/mL):")
mcherry_dilutions = mcherry_concentrations * dilution *  1e-3
print(mcherry_dilutions)

print("\nFinal Concentrations for PelB-mCherry (in µg/mL):")
pelb_dilutions = pelb_mcherry_concentrations * dilution * 1e-3
print(pelb_dilutions)

print("\nmCherry Average:")
print(np.mean(mcherry_dilutions.reshape(3, 3), axis=1))
print("\nmCherry std:")
print(np.std(mcherry_dilutions.reshape(3, 3), axis=1))

print("\nPelB mCherry Average:")
print(np.mean(pelb_dilutions.reshape(3, 3), axis=1))
print("\nPelB mCherry std:")
print(np.std(pelb_dilutions.reshape(3, 3), axis=1))