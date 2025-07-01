import json
from collections import defaultdict
from pathlib import Path


input_json_path = "/Users/rzheng/Desktop/Parse-task1/flux.json"
output_dir = Path("/Users/rzheng/Desktop/Parse-task1/schemas_output")
output_dir.mkdir(parents=True, exist_ok=True)

with open(input_json_path, 'r') as f:
    data = json.load(f)


schemas_by_event_type = defaultdict(list)

for event in data.get("eventTypes", []):
    event_type = event.get("eventTypeIdentifier")
    schema_raw = event.get("schema")
    if event_type and schema_raw:
        try:
            schema = json.loads(schema_raw)
            schemas_by_event_type[event_type].append(schema)
        except json.JSONDecodeError:
            print(f"Invalid JSON in schema for event type: {event_type}")


for event_type, schemas in schemas_by_event_type.items():
    file_path = output_dir / f"{event_type}.json"
    with open(file_path, 'w') as f:
        json.dump(schemas, f, indent=2)
print(len(event_type), "event types found.")
print(f"All schema files saved to: {output_dir.resolve()}")