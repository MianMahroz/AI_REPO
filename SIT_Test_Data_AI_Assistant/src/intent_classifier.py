from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json
import sys
import os

class IntentClassifier:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)

        import os
        model_path = 'models/intent_classifier.pt'
        if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
            self.model.load_state_dict(torch.load(model_path))
        else:
            print("Model file is missing or empty.")

        # self.model.load_state_dict(torch.load('models/intent_classifier.pt'))
        self.model.to(self.device)
        self.model.eval()
        
        with open('training_data/intents.json') as f:
            self.intents = json.load(f)['intents']
        
        self.label_map = {i: intent['tag'] for i, intent in enumerate(self.intents)}
        print("LABEL MAP",self.label_map)

    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        return self.label_map[torch.argmax(outputs.logits, dim=1).item()]

def classify_intent(text):
    return IntentClassifier().classify(text)