import numpy as np
import matplotlib.pyplot as plt

# Generate x values for 10-bit system
x = np.linspace(0, 1024, 1025)

# Parameters
gamma = 2.2

# OETF (Gamma Encoding): simple gamma encoding applied to linear values
def oetf(x, gamma):
    return x ** (1/gamma)

# Gamma encoding
gamma_encoded_values = oetf(x / 1024, gamma) * 1024

# Inverse OETF (Gamma Decoding): converting gamma-encoded values back to linear values
def inverse_oetf(y, gamma):
    return y ** gamma

# Decode gamma-encoded values
linearised_values = inverse_oetf(gamma_encoded_values / 1024, gamma) * 1024

# Create gradient images
gradient_original = np.tile(x, (100, 1)).T
gradient_gamma_encoded = np.tile(gamma_encoded_values, (100, 1)).T
gradient_linearised = np.tile(linearised_values, (100, 1)).T

# Stops for vertical lines (approximate, representing log scale stops)
stops = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Plotting
fig, axs = plt.subplots(2, 3, figsize=(18, 12))

# Function to plot gradients with stops
def plot_gradient_with_stops(ax, gradient, title):
    ax.imshow(gradient, cmap='gray', aspect='auto')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks(stops)
    ax.set_yticklabels([str(s) for s in stops])
    for stop in stops:
        ax.axhline(y=stop, color='red', linestyle='--')
    ax.invert_yaxis()  # Invert y-axis to match the visual example

# Plot gamma-encoded values gradient
plot_gradient_with_stops(axs[1, 0], gradient_gamma_encoded, 'Gamma Encoded (Gamma 2.2)')

# Plot linearised values gradient
plot_gradient_with_stops(axs[1, 1], gradient_linearised, 'Linearised (After Inverse Gamma)')

# Plot original linear values gradient
plot_gradient_with_stops(axs[1, 2], gradient_original, 'Original Linear Values')

# Plot gamma-encoded values curve
axs[0, 0].plot(x, gamma_encoded_values, color='green')
axs[0, 0].set_title('Gamma Encoded (Gamma 2.2)')
axs[0, 0].set_xlabel('Input (Linear Light)')
axs[0, 0].set_ylabel('Output (Gamma Encoded Signal)')
axs[0, 0].set_ylim(0, 1024)
axs[0, 0].grid(True)

# Plot linearised values curve
axs[0, 1].plot(gamma_encoded_values, linearised_values, color='blue')
axs[0, 1].set_title('Linearised (After Inverse Gamma)')
axs[0, 1].set_xlabel('Input (Gamma Encoded Signal)')
axs[0, 1].set_ylabel('Output (Linear Light)')
axs[0, 1].set_ylim(0, 1024)
axs[0, 1].grid(True)

# Plot original linear values curve
axs[0, 2].plot(x, x, color='black')
axs[0, 2].set_title('Original Linear Values')
axs[0, 2].set_xlabel('Input (Linear Light)')
axs[0, 2].set_ylabel('Output (Linear Light)')
axs[0, 2].set_ylim(0, 1024)
axs[0, 2].grid(True)

plt.tight_layout()
plt.show()