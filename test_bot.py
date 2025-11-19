import torch
import json
from model import NeuralNet
from nltk_utils import tokenize, stem, bag_of_words

# Load intents
with open("intents.json", "r") as f:
    intents = json.load(f)

# Load trained model data
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Load model
model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

bot_name = "KTU ChatMe"
print(f"{bot_name} is ready to test intents! Type 'quit' to exit.\n")

while True:
    sentence = input("You: ")
    if sentence.lower() == "quit":
        break

    sentence = tokenize(sentence.lower())
    sentence = [stem(w) for w in sentence]
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    # Prediction
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Print prediction and confidence
    print(f"\n[INFO] Predicted Intent: {tag}")
    print(f"[INFO] Confidence Score: {prob.item():.4f}")

    if prob.item() > 0.5:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(f"{bot_name}: {intent['responses'][0]}")  # first response
    else:
        print(f"{bot_name}: 🤔 I am not confident enough to answer that.\n")
