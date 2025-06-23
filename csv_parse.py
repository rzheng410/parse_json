import json
import csv

with open('flux.json', 'r') as f:
    data = json.load(f)

events = data.get("eventTypes", [])


output_filename = 'customer_activity_events.csv'
fieldnames = [
    "producer_id",
    "event_type_identifier",
    "version",
    "schema_format",
    "partition_key",
    "kafka_topics",
    "requires_archival",
    "publish_to_lce"
]

with open(output_filename, mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for event in events:
        row = {
            "producer_id": event.get("producerId"),
            "event_type_identifier": event.get("eventTypeIdentifier"),
            "version": event.get("version"),
            "schema_format": event.get("schemaFormat"),
            "partition_key": event.get("partitionKey"),
            "kafka_topics": ";".join(event.get("kafkaTopics", [])),
            "requires_archival": event.get("metadata", {}).get("requiresArchival"),
            "publish_to_lce": event.get("metadata", {}).get("publishToLce")
        }
        writer.writerow(row)

print(f" CSV file '{output_filename}' has been created successfully.")