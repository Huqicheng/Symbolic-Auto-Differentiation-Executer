import numpy as np
import autodiff as ad

x = ad.Variable(name = "x")
w = ad.Variable(name = "w")
b = ad.Variable(name = "b")
labels = ad.Variable(name = "lables")


# Computation graph

def cross_entropy(output, labels):
	loss = -1.0 * ad.reduce_sum_op(labels * ad.log_op(output) + (1.0 - labels) * ad.log_op(1.0 - output), axis = 1)
	return loss

# Output of the hypothesis of logistic regression
p = 1.0 / (1.0 + ad.exp_op((-1.0 * ad.matmul_op(w, x))))
# Loss node
loss = cross_entropy(p, labels)
# Gradient node of loss corresponding to w
grad_y_w, = ad.gradients(loss, [w])

num_features = 2
num_points = 200
num_iterations = 1000
learning_rate = 0.01

# The dummy dataset consists of two classes.
# The classes are modelled as a random normal variables with different means.

class_1 = np.random.normal(2, 0.1, (int(num_points / 2), num_features))
class_2 = np.random.normal(4, 0.1, (int(num_points / 2), num_features))
x_val = np.concatenate((class_1, class_2), axis = 0).T

x_val = np.concatenate((x_val, np.ones((1, num_points))), axis = 0)
w_val = np.random.normal(size = (1, num_features + 1))


labels_val = np.concatenate((np.zeros((class_1.shape[0], 1)), np.ones((class_2.shape[0], 1))), axis=0).T
executor = ad.Executor([loss, grad_y_w])

for i in range(100000):
	# evaluate the graph
	loss_val, grad_y_w_val =  executor.run(feed_dict={x:x_val, w:w_val, labels:labels_val})
	# update the parameters using SGD
	w_val = w_val - learning_rate * grad_y_w_val
	if i % 1000 == 0:
		print (loss_val)