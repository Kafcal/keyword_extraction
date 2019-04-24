import numpy as np

def softmax(x):
    exp_x = np.exp(x)
    softmax_x = exp_x / np.sum(exp_x)
    return softmax_x


a = [1,2,3]
print(softmax(a))