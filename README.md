# lookup
Extracts IPv4 addresses from a text file and performs GeoIP/RDAP lookups

## Prerequisites
A `requirements.txt` file has been provided, outlining required libraries. These primarily releate to the flask and requests libraries.
```
pip install -r requirements.txt
```

## Setup
In order to run the program, execute `run.py`. A webpage will be availabe at `http://localhost:5000` for you to interact with it.

## CLI alternative
When prototyping the project, a CLI interface was developed first. This has been retained in the repository in case the Flask app fails to work. To run the CLI version, simply execute `lookup.py`.