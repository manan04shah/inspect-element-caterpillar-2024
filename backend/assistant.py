import json
from fuzzywuzzy import fuzz

conversation_data = json.load(open("conversation_data.json"))

class Assistant:
    language = 'en'

    def start(self, language='en'):
        self.language = language
        print('Assistant started')
        print('Language:', self.language)
    
    def ask_question(self, question):
        print(question['prompt'])
        if question['expected_response']['type'] == 'float':
            return self.get_float_input(question['expected_response']['unit'])
        elif question['expected_response']['type'] == 'str':
            if 'options' in question['expected_response']:
                return self.get_option_input(question['expected_response']['options'])
            else:
                max_length = question['expected_response'].get('max_length', None)
                if max_length:
                    return input(f"Enter your response (max {max_length} characters): ")[:max_length]
                else:
                    return input("Enter your response: ")
        elif question['expected_response']['type'] == 'list':
            items = []
            for i in range(question['expected_response'].get('min_items', 1)):
                items.append(input(f"Enter item {i+1}: "))
            return items
        else:
            return input("Enter your response: ")

    def get_float_input(self, unit):
        while True:
            response = input(f"Enter a number (in {unit}): ")
            try:
                return float(response)
            except ValueError:
                print(f"Invalid input. Please enter a numerical value in {unit}.")

    def get_option_input(self, options):
        print(f"Options: {', '.join(options)}")
        while True:
            response = input("Enter your choice: ").strip().lower()
            best_match = max(options, key=lambda x: fuzz.ratio(response, x.lower()))
            if fuzz.ratio(response, best_match.lower()) >= 80:
                print(f"Understood: {best_match}")
                return best_match
            print("Invalid option. Please try again.")

    def ask_tire_questions(self):
        print("Let's start with the TIRES inspection.")
        for question in conversation_data["TIRES"]["questions"]:
            response = self.ask_question(question)
            print(f"Recorded response for {question['id']}: {response}")
        print("TIRES inspection completed.")

if __name__ == '__main__':
    # Create a new instance of the Assistant class
    assistant = Assistant()

    # Start the assistant
    assistant.start()

    assistant.ask_tire_questions()