import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# use GPU if available else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# intent_file = input("Enter the name of the intents file: ")

FILE = "data.pth"
data = torch.load(FILE)

# load the hyper params and model_state from the saved file
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]
intent_file = data["intent_file"]

with open(intent_file, 'r') as f:
    intents = json.load(f)

model = NeuralNet(input_size, hidden_size, output_size).to(device)
# load the weights after training before
model.load_state_dict(model_state)
# set the model to evaluation mode
model.eval()

bot_name = "PyBot"


def get_response(msg):
    msg = msg.lower()
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    # reshape to the shape required by the model ie 1 row and <len(all_words)> columns
    X = X.reshape(1, X.shape[0])
    # creates a tensor from X
    X = torch.from_numpy(X)

    # get the model output, which will basically contain the output values for all the tags
    output = model(X)
    # reduce to 1 dimension
    _, predicted = torch.max(output, dim=1)
    # (predicted is a tensor with index of the highest output valuethe and .item() gives the content inside it
    #  bascially what is the index of the tag with highest output
    tag = tags[predicted.item()]

    # convert the output value of the model to probablities using softmax activation function
    # dim = 1 to get 1 dimensional output, we're dealing with 1-D anyways
    probs = torch.softmax(output, dim=1)
    # now pick the highest probability
    prob = probs[0][predicted.item()]

    # check if there's a 50% probability that the user's input is similar to the patterns in the predicted tag
    # if yes, then return a random response from the tag, else return "do not understand"
    if prob.item() > 0.50:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return tag

    else:
        return "noans"
