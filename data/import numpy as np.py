import numpy as np

def equation(x):
    # Parameters to control the curve's steepness and behavior
    A = 10**8  # Growth factor, controls how fast the function increases
    B = 0.05   # Steepness factor, larger B makes the rise sharper
    C = 500    # The value of x at which the function starts rising rapidly
    D = 30     # Starting offset value
    
    # Ensure the result starts at D and grows as expected
    return 30*np.exp(0.1*x)



# Test the function with an array of values
x_values = np.arange(0, 50)
results = equation(x_values)
print("Results for x_values:", x_values)
print(results)
print(len(results))
