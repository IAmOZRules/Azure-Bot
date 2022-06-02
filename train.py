import json
import numpy as np
from termcolor import colored

import torch
import torch.nn as nn
from nltk_utils import tokenize, stem, bag_of_words
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet


def trainModel(intent_file):
    # Opens the intents.json file
    with open(intent_file, 'r') as f:
        intents = json.load(f)

    ignore_words = ['?', "!", ".", ","]
    all_words = []
    tags = []
    # xy will contain tokenized pattern sentence with it's respective tag
    xy = []

    print(colored("\n<-- Initializing Model Training -->", "red"))

    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            w = tokenize(pattern)
            all_words.extend(w)
            xy.append((w, tag))

    all_words = [stem(w) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    X_train = []
    Y_train = []

    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)                 # Feature Set
        label = tags.index(tag)
        Y_train.append(label)               # Label Set

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    class ChatDataSet(Dataset):
        def __init__(self):
            self.n_samples = len(X_train)
            self.x_data = X_train
            self.y_data = Y_train

        # dataset(idx)
        def __getitem__(self, index):
            return (self.x_data[index], self.y_data[index])

        def __len__(self):
            return self.n_samples

    # Hyperparameters
    batch_size = 8
    hidden_size = 8
    output_size = len(tags)
    input_size = len(X_train[0])
    learning_rate = 0.001
    num_epochs = 1000

    dataset = ChatDataSet()
    train_loader = DataLoader(
        dataset=dataset, batch_size=batch_size, shuffle=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(input_size, hidden_size, output_size)

    # Measures the performance of the classification model (loss)
    # Greater Cross Entropy Loss means greater probability divergence from the actual label
    criterion = nn.CrossEntropyLoss()

    # Model Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Repeatedly trains the model for a set amount of times
    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)

            # Forward Pass Step for the Neural Network
            outputs = model(words)
            loss = criterion(outputs, labels.long())

            # Emptying the gradients before beginning backward pass
            optimizer.zero_grad()

            # Backward Pass Step for the Neural Network
            loss.backward()

            # update the parameters by gradient descent
            optimizer.step()

        # Print results after every 100 epochs
        if (epoch + 1) % 100 == 0:
            print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

    print(colored("<-- Model Training Completed -->", "red"))
    print(f'\nFinal loss, loss={loss.item():.4f}')

    # Save the data into a file so that the chatbot can use it later
    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags,
        "intent_file": intent_file
    }

    FILE = "data.pth"
    torch.save(data, FILE)

    print(f"Training Data saved to", colored(FILE, "green"))

trainModel('json/ion.json')