"""
Project: Visualization.
Second code file.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("SwissGDP_Final2.csv")

print(df.shape)
print(df.dtypes)
print(df.describe())
print(df.isna().sum())
df.fillna(df.mean(), inplace=True)

df.drop(['Indicator Code'], axis=1, inplace=True)

# =============================================================================
# scaler = StandardScaler()
# df_scaled = scaler.fit_transform(df.iloc[:,1:])
# =============================================================================


# =============================================================================
# #Calculate the correlation matrix:
# corr_matrix = df.corr()
# 
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
# plt.show()
# 
# 
# print(df.corr())
# =============================================================================

# Transposing the dataFrame so that each row corresponds to an indicator

df_t = df.set_index('Indicator Name').T

# Select the row corresponding to 'GDP (constant LCU)'
gdp_row = df_t['GDP (constant LCU)']

# Compute the correlations between 'GDP (constant LCU)' and the other rows
corr = df_t.corrwith(gdp_row)

# Plot the correlations as a bar chart
corr.plot(kind='bar', figsize=(10, 6))
plt.title("Correlation with 'GDP (constant LCU)'")
plt.xlabel('Indicator')
plt.ylabel('Correlation')
plt.show()

# Transposing the dataFrame so that each row corresponds to an indicator

df_t = df.set_index('Indicator Name').T

# Compute the correlations between all pairs of indicators
corr = df_t.corr()

# Plot a heatmap of the correlations
sns.heatmap(corr, cmap='coolwarm')
plt.title('Correlations')
plt.show()
