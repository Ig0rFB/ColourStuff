import numpy as np


def create_1d_lut(size, transformation_function):
    input_range = np.linspace(0.0, 1.0, size)
    output_values = transformation_function(input_range)
    return dict(zip(input_range, output_values))

def my_function_r(x):
    return x**2  

def my_function_g(x):
    return x  

def my_function_b(x):
    return x**0.5  

input_rgb = [0.5, 0.2, 0.8]

lut_r = create_1d_lut(size=256, transformation_function=my_function_r)
lut_g = create_1d_lut(size=256, transformation_function=my_function_g)
lut_b = create_1d_lut(size=256, transformation_function=my_function_b)

def interpolate(x, x_values, y_values):
    idx = np.searchsorted(x_values, x)
    if idx == 0:
        return y_values[0]
    elif idx == len(x_values):
        return y_values[-1]
    else:
        x0, x1 = x_values[idx - 1], x_values[idx]
        y0, y1 = y_values[idx - 1], y_values[idx]
        return y0 + (x - x0) * (y1 - y0) / (x1 - x0)

output_r = interpolate(input_rgb[0], list(lut_r.keys()), list(lut_r.values()))
output_g = interpolate(input_rgb[1], list(lut_g.keys()), list(lut_g.values()))
output_b = interpolate(input_rgb[2], list(lut_b.keys()), list(lut_b.values()))

output_rgb = [output_r, output_g, output_b]

print("Input RGB:", input_rgb)
print("Output RGB:", output_rgb)

#ws test