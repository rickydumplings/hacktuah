# main.py (python example)

import os
from dotenv import load_dotenv
import json

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

# Path to the audio file
AUDIO_FILE = "1780 Le Roy Ave, Unit 1.m4a"

API_KEY = os.getenv("API_KEY")


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            detect_entities=True
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        # print(response.to_json(indent=4))

        # response = response.to_json(indent=4)

        entities = response['results']['channels'][0]['alternatives'][0]["entities"]
        print(entities)

        accumulate = {}

        for entity in entities:
            print(entity)
            if entity['label'] == "NAME":
                accumulate['name'] = entity['value']
            if entity['label'] == "LOCATION_ADDRESS":
                accumulate['location'] = entity['value']


        if not accumulate['name']:
            accumulate['name'] = "NONE"
        if not accumulate['location']:
            accumulate['location'] = "NONE"


        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]

        # Print the transcript
        print(transcript)

        def generate(input, target):
            vertexai.init(project="gen-lang-client-0421443332", location="us-central1")
            model = GenerativeModel(
                "gemini-1.5-flash-002",
            )
            responses = model.generate_content(
                [input],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )

            response_texts = ""

            # STEP 5: Collect response texts
            for response in responses:
                print(response.text, end="")
                response_texts += response.text

            # print(response_texts)
            accumulate[target] = response_texts

        text1 = f"""You are analyzing an emergency call transcript. Your task is to extract and summarize the three most critical pieces of information from the call. Focus only on essential details, and **omit any extraneous or irrelevant information**, such as mentions of relationships or unnecessary repetition of urgency. Specifically:

        1. The nature of the emergency or danger.
        2. Any critical health conditions or relevant medical history.
        3. Any environmental hazards (e.g., electrical hazards, fire, dangerous surroundings).
        4. Other important symptoms or events leading up to the emergency.

        The summary must consist of **three sentences**, each limited to 5-6 words. Avoid unnecessary personal references and focus only on the core details that are medically or contextually important. Include environmental hazards if they are relevant to the situation.

        Here is the transcript: 
        {transcript}
        Please provide a concise summary in **three sentences, each containing 5-6 words**. Include environmental hazards if they are relevant to the situation, and focus on symptoms, conditions, and context."""

        text2 = f"""You are analyzing a 911 call transcript. Your task is to recommend the three most critical actions a first responder should take upon arrival. Focus only on essential details and **omit any extraneous or irrelevant information**, such as relationships or unnecessary repetition of urgency. Specifically:

        1. Address the immediate medical needs of the individual.
        2. Ensure the safety of the first responder and the public.
        3. Consider the need for additional resources or transport.

        The recommendation must consist of **three concise actions**, each limited to 7-10 words. Avoid unnecessary personal references and focus only on the core actions that are crucial for medical or contextual reasons. Environmental hazards should be mentioned if relevant.

        Here is the transcript:
        {transcript}

        Please provide three action steps in **4-5 words each**, addressing the individual's medical needs, responder safety, and resource considerations. Each point should be divided into sentences, not bullet points or lists.""" 


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

        generate(text1, "summary")
        generate(text2, "actions")

        # STEP 6: Save the responses to a JSON file
        with open("api_result.json", "w") as json_file:
            json.dump(accumulate, json_file, indent=4)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()


# # Specify the file name
# file_name = "api_result.json"

# # Write the result to a JSON file
# with open(file_name, 'w') as json_file:
#     json.dump(response.to_json(indent=4), json_file, indent=4)

# print(f"API result saved to {file_name}")

# entities = response['results']['channels'][0]['alternatives'][0]["entities"]

# # Extract and print the labels
# # labels = [entity['label'] for entity in entities]
# # print(labels)
# print(entities)
