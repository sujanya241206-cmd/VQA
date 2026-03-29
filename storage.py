import json
import os

class StorageManager:

    def __init__(self):
        self.file = "history.json"
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f)

    def save_history(self, username, image, question, answer, story):
        with open(self.file, "r") as f:
            data = json.load(f)

        if username not in data:
            data[username] = []

        data[username].append({
            "image": image,
            "question": question,
            "answer": answer,
            "story": story
        })

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def get_user_history(self, username):
        with open(self.file, "r") as f:
            data = json.load(f)

        return data.get(username, [])
