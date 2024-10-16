#%%
import matplotlib.pyplot as plt
import numpy as np

# Sample data: a list of numbers
data = np.random.random_sample((100,))

# Sort data to facilitate upward jittering
data.sort()

# Initialize y-values at zero
y_values = np.zeros(len(data))

# Define the minimum distance to avoid overlap
min_distance = 0.01

# Apply jitter: move points up only if they overlap
for i in range(1, len(data)):
    if data[i] == data[i - 1]:
        y_values[i] = y_values[i - 1] + min_distance

# Create a scatter plot with flipped axes
plt.figure(figsize=(2, 8))  # Adjusted figure size for vertical layout
plt.scatter(y_values, data, alpha=0.5)  # Swap x and y values

# Set plot labels and title
plt.ylabel('Values')
plt.title('One-Dimensional Scatter Plot with Upward Jitter')

# Remove x-axis as it's not meaningful in this context
plt.xticks([])

# Show the plot
plt.show()
# %%
