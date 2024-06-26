import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 1024, 1025)
gamma = 2.2

def oetf(x, gamma):
    return x ** (1/gamma)

def eotf(y, gamma):
    return y ** gamma


oetf_values = oetf(x / 1024, gamma) * 1024 # Compute OETF values and normalise x to [0, 1] and scale output back to [0, 1024]

# Convert to 10-bit greyscale values
original_greyscale_values = np.round(x).astype(np.uint16)
oetf_greyscale_values = np.round(oetf_values).astype(np.uint16)

# Create gradient images and invert them
gradient_original = np.tile(original_greyscale_values, (100, 1)).T
gradient_oetf = np.tile(oetf_greyscale_values, (100, 1)).T

# Compute EOTF values for plotting
eotf_values = eotf(x / 1024, gamma) * 1024  # Normalize x to [0, 1] and scale output back to [0, 1024]
stops = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

fig, axs = plt.subplots(1, 3, figsize=(18, 12), gridspec_kw={'width_ratios': [1, 2, 1]})


def plot_gradient_with_stops(ax, gradient, title, is_log_scale=False): #plot gradients with stops
    ax.imshow(gradient, cmap='gray', aspect='auto')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks(stops)
    ax.set_yticklabels([str(s) for s in stops])
    for stop in stops:
        ax.axhline(y=stop, color='red', linestyle='--')
    ax.invert_yaxis()  # Invert y-axis to match the visual example
    if is_log_scale:
        ax.set_yscale('log')

plot_gradient_with_stops(axs[0], gradient_original, 'Linear', is_log_scale=False)

# Plot EOTF curve
axs[1].plot(x, x, color='gray', linestyle='--')
axs[1].plot(x, eotf_values, color='blue')
axs[1].set_title('EOTF')
axs[1].set_xlabel('Input')
axs[1].set_ylabel('Output')
axs[1].grid(True)


plot_gradient_with_stops(axs[2], gradient_oetf, 'Logarithmic', is_log_scale=True)

plt.tight_layout()
plt.show()