import numpy as np
import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(0, 1, 256)

# Parameters
gamma = 2.2

# OETF: simple gamma encoding
def oetf(x, gamma):
    return x ** (1/gamma)

# EOTF: inverse gamma encoding
def eotf(x, gamma):
    return x ** gamma

# Compute OETF and EOTF values
oetf_values = oetf(x, gamma)
eotf_values = eotf(x, gamma)

# Convert to 8-bit greyscale values
oetf_greyscale_values = np.round(oetf_values * 255).astype(np.uint8)
eotf_greyscale_values = np.round(eotf_values * 255).astype(np.uint8)

# Create gradient images and invert them
gradient_oetf = np.tile(oetf_greyscale_values, (256, 1)).T[::-1]
gradient_eotf = np.tile(eotf_greyscale_values, (256, 1)).T[::-1]

# Stops for vertical lines (approximate)
stops = [0, 32, 64, 128, 256]

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 12))

# Function to plot gradients with stops
def plot_gradient_with_stops(ax, gradient, title):
    ax.imshow(gradient, cmap='gray', aspect='auto')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks(stops)
    ax.set_yticklabels([f'{2**i}' for i in range(len(stops))])
    for stop in stops:
        ax.axhline(y=stop, color='red', linestyle='--')
    ax.invert_yaxis()  # Invert y-axis to match the visual example

# Plot OETF curve and gradient
axs[0, 0].plot(x, oetf_values, color='black')
axs[0, 0].set_title('OETF Curve (Gamma Encoding)')
axs[0, 0].set_xlabel('Input (Linear Light)')
axs[0, 0].set_ylabel('Output (Electrical Signal)')
plot_gradient_with_stops(axs[0, 1], gradient_oetf, 'Gradient with OETF')

# Plot EOTF curve and gradient
axs[1, 0].plot(x, eotf_values, color='black')
axs[1, 0].set_title('EOTF Curve (Gamma Decoding)')
axs[1, 0].set_xlabel('Input (Electrical Signal)')
axs[1, 0].set_ylabel('Output (Linear Light)')
plot_gradient_with_stops(axs[1, 1], gradient_eotf, 'Gradient with EOTF')

plt.tight_layout()
plt.show()