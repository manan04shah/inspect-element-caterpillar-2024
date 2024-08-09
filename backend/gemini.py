import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# response  = model.generate_content("I am going to give you data from the safety inspection and maintenance of a construction equipment vehicle, by the Caterpillar inc. company. Based on this, suggest a 5 more checks I should ask the technician to make on the vehicle, and what alert does that help solve. Here is the data: Tire Data: pressure_left_front: 30.0, pressure_right_front: 30.0, condition_left_front: 'good', condition_right_front: 'good', pressure_left_rear: 30.0, pressure_right_rear: 30.0, condition_left_rear: 'good', condition_right_rear: 'good', Battery Data: make: 'Caterpillar', replacement_date: '2022-01-01', voltage: '12V', water_level: 'good', damage: False, leak_or_rust: False, Exterior Data: rust_or_damage: False, oil_leak_in_suspension: False, Brakes Data: fluid_level: 'good', condition_front: 'good', condition_rear: 'good', emergency_brake: 'good', Engine Data: rust_or_damage: False, oil_condition: 'good', oil_color: 'clear', fluid_condition: 'good', fluid_color: 'clear', oil_leak: False")
# print(response.text)

def gemini_custom_prompt(prompt):
    response = model.generate_content(prompt)
    return response.text

def inspect_tyres(tire_data, equipment_type):
    prompt = f"I am going to give you data from the safety inspection and maintenance of a construction equipment vehicle which is a {equipment_type}, by the Caterpillar inc. company. This data is basically what the technician said while inspecting the tyres. Based on this, give me a nice (<1000 word) summary about the tyre status. Include all relevant information, get as detailed as possible. Use as many numbers and performance metrics as you can. No beating around the bush. I need a very helpful summary, keep response as key:value as far as possible rather than using text emphasis, bold and all. Here is the data: Tire Data: pressure_left_front: {tire_data['pressure_left_front']}, pressure_right_front: {tire_data['pressure_right_front']}, condition_left_front: '{tire_data['condition_left_front']}', condition_right_front: '{tire_data['condition_right_front']}', pressure_left_rear: {tire_data['pressure_left_rear']}, pressure_right_rear: {tire_data['pressure_right_rear']}, condition_left_rear: '{tire_data['condition_left_rear']}', condition_right_rear: '{tire_data['condition_right_rear']}'"
    return gemini_custom_prompt(prompt)