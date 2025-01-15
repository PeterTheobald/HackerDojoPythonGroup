Serialization and Transmission

## Why?
1. *STORE* data for later
2. *SEND* data to another service

## tl;dr the best
You will probably use JSON, Pickle or Protobufs for most use cases

## Formats

Text formats:
human readable, easy to debug, easy to manually enter and edit
- TEXT or CSV - simple, human readable, interop with spreadsheets, TERRIBLE for complex data types
- JSON - Not all complex data types, mostly lists and dicts. Standard: Interop with other systems. SAFE!
- YAML (PyYaml library) mostly used for config files
- XML

Binary formats:
not human readble, but *fast* and *compact*
- Pickle - Native, built-in, any complex Python data structure. DANGEROUS EVAL!
    - alternatives: Marshal (faster but not all data types), Dill (more data types)
- Google Protobuf - efficient fast compact with schema for data layout and types
- Apache Thrift - compact binary schema used by Meta
- avro - efficient, built in schema
- BSON, MessagePack - binary versions of JSON
- Google FlatBuffers - very fast, used by games and real-time systems

Specialized formats:
- HDF5 - very large hierarchical data sets, machine learning, scientific computing
- Apache Parquet - standard for Pandas big data storage (pandas & pyarrow)
- Feather: fast binary format for Panda dataframes (pandas & pyarrow)

## hand-written serialization

- Write data to .txt or .csv manually

```
import csv

# Data to write
data = [
    {"Name": "Alice", "Age": 30, "City": "New York"},
    {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
    {"Name": "Charlie", "Age": 35, "City": "Chicago"}
]

# Write data to CSV
with open("data.csv", "w", newline="") as csvfile:
    fieldnames = ["Name", "Age", "City"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write the data rows
```


## Pickle
- Pickle: convert data to byte-stream
- Unpickle: convert byte-stream to data
- Danger do not unpickle bytes from external sources. Can execute arbitrary code!
- Not portable, not even between different versions of Python

```
import pickle

# Pickling
data = {"key": "value", "number": 42}
with open("data.pkl", "wb") as file:
    pickle.dump(data, file)

# Unpickling
with open("data.pkl", "rb") as file:
    loaded_data = pickle.load(file)
print(loaded_data)
```

## JSON

```
import json

# Data to be serialized
data = {"key": "value", "number": 42, "items": [1, 2, 3]}

# Writing JSON data to a file
with open("data.json", "w") as file:
    json.dump(data, file)

# Reading JSON data back from the file
with open("data.json", "r") as file:
    loaded_data = json.load(file)

# Output the loaded data
print(loaded_data)
```


## Database

- Manually save data to a SQL database: sqlite, MySql, etc.
- Use an ORM to convert data structures to SQL: SQLAlchemy, Django ORM
- Manually save JSON to a document/Object database: pyMongo, redis-py, Cassandra, AWS S3 (boto3) 
- Redis: fast in-memory database
- ZODB: Object oriented database for Python saves python objects directly without a schema

## Message queues

- Stores high speed and volume of data in a queue for async writing to another datastore
- RabbitMQ, Kafka

## Google Protobuf

1. Define your schema: example.proto
```
syntax = "proto3";

message Person {
  string name = 1;
  int32 age = 2;
  repeated string hobbies = 3;
}
```

2. Compile your schema to generated Python code:
example.proto => example_pb2.py
```
protoc --python_out=. example.proto
```

3. Use Protobuf with schema:
```
import example_pb2

# Create a Person message
person = example_pb2.Person()
person.name = "Alice"
person.age = 30
person.hobbies.extend(["Reading", "Cycling", "Hiking"])

# Serialize the Person message to a binary file
with open("person.bin", "wb") as file:
    file.write(person.SerializeToString())


# Read the binary file and deserialize the Person message
with open("person.bin", "rb") as file:
    person_data = file.read()

# Create a Person instance and parse the binary data
person = example_pb2.Person()
person.ParseFromString(person_data)

# Output the deserialized data
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Hobbies: {', '.join(person.hobbies)}")

```

