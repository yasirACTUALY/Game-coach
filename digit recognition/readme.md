basic first practice to learn how an ai model learns and the basics of a nueral network.
there are first a row of nodes which represent every input we pass on usually in the form of a number between 0-1 representing the value of a specific input.
Then comes the hidden layers which consists of 1 more nodes, each node connects to 1 or more input nodes and uses the node value then multiply it by a weight and adds a constant to determin the hiddeb node value(also from 0-1).
finally a the output layer which consists of as many nodes as there is apossible outputs and each node will have a value from 0-1, which represents the the chance of this output being the right one based on the model.A 1 meaning the model is 100% sure this is the right output. Also if you add all the outputs nodes value you get a 1(for 100%)

More to know:
We could have as many hidden layers and hidden nodes as we want but only on output and input layers.
The learning process is simply changing the weights and the constants for each node until the hidden nodes can proficently convey the correct output to the outputlayer
The process of changing the weights and constants is called backprobagation which is basically going back and using the error(the corrent output - the correct ouput) for each output node and going backwards through each layer and calculating the derivative of the error with respect to the weights and using that to change the weights so that the error approaches 0
