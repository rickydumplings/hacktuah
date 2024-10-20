import json
from collections import defaultdict

# Load the original JSON from the file
with open('api_result.json', 'r') as file:
    data = json.load(file)


print(data)
# Initialize a dictionary to store the grouped entities
grouped_entities = defaultdict(list)

# Assuming the entities are located in the "entities" key within the JSON structure
for channel in data.get("results", {}).get("channels", []):
    for alternative in channel.get("alternatives", []):
        for entity in alternative.get("entities", []):
            # Extract the label and value of each entity
            label = entity.get("label", "")
            value = entity.get("value", "")
            
            # Append the value under the corresponding label
            grouped_entities[label].append(value)

# Convert defaultdict to a regular dict
grouped_entities = dict(grouped_entities)

# Write the grouped entities into a new JSON file
with open('grouped_entities.json', 'w') as output_file:
    json.dump(grouped_entities, output_file, indent=4)

print("Entities have been grouped and saved to 'grouped_entities.json'.")