import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import json

# Load the JSON file
with open('api_result.json', 'r') as file:
    data = json.load(file)

print(data)

# Extract the transcript
transcript = data
# transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]

# Print the transcript
print(transcript)

def generate():
    vertexai.init(project="gen-lang-client-0421443332", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")

text1 = f"""You are analyzing an emergency call transcript. Your task is to extract and summarize the three most critical pieces of information from the call. Focus only on essential details, and **omit any extraneous or irrelevant information**, such as mentions of relationships or unnecessary repetition of urgency. Specifically:

1. The nature of the emergency or danger.
2. Any critical health conditions or relevant medical history.
3. Any environmental hazards (e.g., electrical hazards, fire, dangerous surroundings).
4. Other important symptoms or events leading up to the emergency.

The summary must consist of **three sentences**, each limited to 5-6 words. Avoid unnecessary personal references and focus only on the core details that are medically or contextually important. Include environmental hazards if they are relevant to the situation.

Here is the transcript: 
{transcript}
Please provide a concise summary in **three sentences, each containing 5-6 words**. Include environmental hazards if they are relevant to the situation, and focus on symptoms, conditions, and context."""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

generate()