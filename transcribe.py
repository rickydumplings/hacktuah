import os
from dotenv import load_dotenv
import json

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()
# print(os.getcwd())

# URL to the audio file
AUDIO_URL = {
    "url": "https://dpgr.am/spacewalk.wav"
}

# Path to the audio file
AUDIO_FILE = "1780 Le Roy Ave, Unit 1.m4a"

API_KEY = os.getenv("API_KEY")

def main():
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            detect_entities=True,
            punctuate=True,
            summarize="v2",
            detect_topics=True
        )

        # STEP 3: Call the transcribe_url method with the audio payload and options
        # response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)

        #  STEP 3: Call the transcribe_file method with the audio payload and options
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # print("Hello?")

        # STEP 4: Print the response
        # print(response.to_json(indent=4))
        print(response["results"]["channels"][0]["alternatives"][0]["transcript"])

        
        # Specify the file name
        file_name = "api_result.json"

        # Write the result to a JSON file
        with open(file_name, 'w') as json_file:
            json.dump(response.to_json(indent=4), json_file, indent=4)

        print(f"API result saved to {file_name}")

        entities = response['results']['channels'][0]['alternatives'][0]["entities"]

        # Extract and print the labels
        # labels = [entity['label'] for entity in entities]
        # print(labels)
        print(entities)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()