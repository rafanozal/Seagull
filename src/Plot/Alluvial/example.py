import core
import matplotlib.pyplot as plt
#import numpy as np

input_data = {'a': {'aa': 0.3, 'cc': 0.7,},
              'b': {'aa': 2, 'bb': 0.5,},
              'c': {'aa': 0.5, 'bb': 0.5, 'cc': 1.5,}}

ax = core.plot(input_data)
fig = ax.get_figure()
fig.set_size_inches(5,5)
plt.show()


input_data = {'a': {'aa': 200, 'cc': 300,},
              'b': {'aa': 50, 'bb': 100,},
              'c': {'aa': 50, 'bb': 100, 'cc': 500,}}

ax = core.plot(input_data)
fig = ax.get_figure()
fig.set_size_inches(5,5)
plt.show()