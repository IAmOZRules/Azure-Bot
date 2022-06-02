import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)    # Input Layer
        self.l2 = nn.Linear(hidden_size, hidden_size)   # Hidden Layer 1
        self.l3 = nn.Linear(hidden_size, num_classes)   # Hidden Layer 2
        
        """
        Rectified Linear Unit Activation function
        ReLU returns the value if it is greater than zero, or 0 if value less than zero
        """
        self.relu = nn.ReLU()

    # Forward pass function
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)    # Pass output from layer 1 to layer 2
        out = self.l2(out)
        out = self.relu(out)    # Pass output from layer 2 to layer 3
        out = self.l3(out)
        
        """
        No Activation or SoftMax function required
        CrossEntropyLoss does that on its own
        """

        return out