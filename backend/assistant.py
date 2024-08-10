import json
from fuzzywuzzy import fuzz


class Assistant:
    language = 'en'

    def start(self, language='en'):
        self.language = language
        print('Assistant started')
        print('Language:', self.language)
        self.conversation_data = json.load(open("conversation_data.json"))

    
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

    def add_custom_context(self):
        print("Adding custom inspection item")
        
        # Get the category name
        category_name = input("Enter the name of the new category: ").upper()
        
        # Initialize the new category
        new_category = {
            "questions": []
        }
        
        # Add questions to the category
        while True:
            question = {}
            question["id"] = input("Enter question ID (e.g., custom_item_condition): ")
            question["prompt"] = input("Enter the question prompt: ")
            
            # Get the expected response type
            response_type = input("Enter the expected response type (float/str/bool/list): ").lower()
            
            expected_response = {"type": response_type}
            
            if response_type == "float":
                expected_response["unit"] = input("Enter the unit for the float value: ")
            elif response_type == "str":
                options = input("Enter options separated by comma (leave blank if no options): ")
                if options:
                    expected_response["options"] = [opt.strip() for opt in options.split(",")]
                else:
                    max_length = input("Enter maximum length for the string (leave blank if no limit): ")
                    if max_length:
                        expected_response["max_length"] = int(max_length)
            elif response_type == "list":
                expected_response["item_type"] = input("Enter the type of items in the list: ")
                expected_response["min_items"] = int(input("Enter the minimum number of items: "))
                expected_response["max_items"] = int(input("Enter the maximum number of items: "))
            
            question["expected_response"] = expected_response
            
            new_category["questions"].append(question)
            
            if input("Add another question? (y/n): ").lower() != 'y':
                break
        
        # Add the new category to conversation_data
        self.conversation_data[category_name] = new_category
        
        # Save the updated conversation_data to the JSON file
        with open("conversation_data.json", "w") as f:
            json.dump(self.conversation_data, f, indent=2)
        
        print(f"New category '{category_name}' has been added to conversation_data.json")



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


    def load_custom_category(self):
        file_name = input("Enter the name of the JSON file containing the custom category: ")
        if not file_name.endswith('.json'):
            file_name += '.json'
        
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r') as f:
                    custom_category = json.load(f)
                
                if isinstance(custom_category, dict) and "questions" in custom_category:
                    category_name = input("Enter a name for this category: ").upper()
                    self.conversation_data[category_name] = custom_category
                    print(f"Custom category '{category_name}' has been loaded successfully.")
                    
                    # Save the updated conversation_data to the JSON file
                    with open("conversation_data.json", "w") as f:
                        json.dump(self.conversation_data, f, indent=2)
                else:
                    print("Invalid file format. The JSON file should contain a category with a 'questions' key.")
            except json.JSONDecodeError:
                print("Invalid JSON file. Please check the file format.")
        else:
            print(f"File '{file_name}' not found.")


    def perform_inspection(self):
        while True:
            print("\nMain Menu:")
            print("1. Perform Inspection")
            print("2. Add Custom Category")
            print("3. Load Custom Category")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.inspect_categories()
            elif choice == '2':
                self.add_custom_context()
            elif choice == '3':
                self.load_custom_category()
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

    def inspect_categories(self):
        print("\nAvailable categories for inspection:")
        categories = list(self.conversation_data.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        while True:
            try:
                choice = int(input("Enter the number of the category you want to inspect (0 to return to main menu): "))
                if choice == 0:
                    break
                if 1 <= choice <= len(categories):
                    selected_category = categories[choice - 1]
                    self.ask_category_questions(selected_category)
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")



    def ask_category_questions(self, category):
        print(f"\nStarting {category} inspection.")
        for question in self.conversation_data[category]["questions"]:
            response = self.ask_question(question)
            print(f"Recorded response for {question['id']}: {response}")
        print(f"{category} inspection completed.\n")



if __name__ == '__main__':
    assistant = Assistant()
    assistant.start()
    assistant.perform_inspection()
