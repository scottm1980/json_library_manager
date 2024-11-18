import os
import json
from openai import OpenAI
import sys
import re
from pathlib import Path
from logger import setup_logger
from jsonschema import validate, ValidationError

# Initialize logger
logger = setup_logger('ProjectInitializer', 'project_initializer.log')

# Ensure OpenAI API key is set
client = OpenAI()
if not client.api_key:
    logger.critical("OPENAI_API_KEY environment variable not set.")
    sys.exit("Please set the OPENAI_API_KEY environment variable.")

def load_subject(file_path='alignment_files/subject.json'):
    """Load the game description from subject.json."""
    logger.debug(f"Loading subject from {file_path}")
    if not Path(file_path).is_file():
        logger.error(f"{file_path} does not exist.")
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path, 'r') as f:
        try:
            subject = json.load(f)
            if 'subject_description' not in subject:
                logger.error("subject_description key not found in subject.json.")
                raise KeyError("subject_description key not found in subject.json.")
            logger.info("Loaded subject description.")
            return subject['subject_description']
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding {file_path}: {e}")
            raise

def save_json(data, filename):
    """Save a dictionary as a JSON file."""
    logger.debug(f"Saving data to {filename}")
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved {filename}")
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise

def extract_json(content):
    """
    Extract JSON content from a string, removing any markdown code block delimiters.
    """
    logger.debug("Extracting JSON content from string")
    # Remove ```json and ``` if present
    json_pattern = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)
    match = json_pattern.search(content)
    if match:
        return match.group(1).strip()
    
    # Remove generic code block delimiters if present
    json_pattern_generic = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)
    match_generic = json_pattern_generic.search(content)
    if match_generic:
        return match_generic.group(1).strip()
    
    # If no code block, return the content as is
    return content.strip()

def generate_structure(subject_description):
    """Generate structure.json using OpenAI."""
    logger.debug("Generating structure.json using OpenAI")
    prompt = f"""
Analyze the following game description and provide a JSON structure outlining the key screens, features, and components.

Description:
{subject_description}

**Do not include any code block delimiters. Provide only the JSON content.**
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating game configuration files."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        raw_content = response.choices[0].message.content.strip()
        cleaned_content = extract_json(raw_content)
        structure = json.loads(cleaned_content)
        logger.info("Generated structure.json successfully.")
        return structure
    except Exception as e:
        logger.error(f"Error generating structure.json: {e}")
        logger.debug(f"Received response: {raw_content}")
        raise

def generate_models(structure_json):
    """Generate models.json using OpenAI."""
    logger.debug("Generating models.json using OpenAI")
    prompt = f"""
Based on the following app structure, define the necessary data models in JSON format. Include model names and their fields with types.

App Structure:
{json.dumps(structure_json, indent=4)}

**Do not include any code block delimiters. Provide only the JSON content.**
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating game configuration files."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        raw_content = response.choices[0].message.content.strip()
        cleaned_content = extract_json(raw_content)
        models = json.loads(cleaned_content)
        logger.info("Generated models.json successfully.")
        return models
    except Exception as e:
        logger.error(f"Error generating models.json: {e}")
        logger.debug(f"Received response: {raw_content}")
        raise

def generate_other_values(subject_json, structure_json, models_json):
    """Generate OtherValues.json using OpenAI."""
    logger.debug("Generating OtherValues.json using OpenAI")
    prompt = f"""
Based on the following subject, structure, and models, generate a JSON file containing predefined events, states, function signatures, and other reusable values.

Subject:
{json.dumps({"subject_description": subject_json}, indent=4)}

Structure:
{json.dumps(structure_json, indent=4)}

Models:
{json.dumps(models_json, indent=4)}

**Do not include any code block delimiters. Provide only the JSON content.**
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating game configuration files."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        raw_content = response.choices[0].message['content'].strip()
        cleaned_content = extract_json(raw_content)
        other_values = json.loads(cleaned_content)
        logger.info("Generated OtherValues.json successfully.")
        return other_values
    except Exception as e:
        logger.error(f"Error generating OtherValues.json: {e}")
        logger.debug(f"Received response: {raw_content}")
        raise

def generate_state_report(file_name, status, details):
    """Generate or update a state report."""
    logger.debug(f"Generating state report for {file_name}")
    report_entry = {
        "file": file_name,
        "status": status,
        "details": details
    }
    report_path = Path('state_report.json')
    try:
        if report_path.is_file():
            with open(report_path, 'r') as f:
                report_data = json.load(f)
        else:
            report_data = []
        report_data.append(report_entry)
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        logger.info(f"State report updated for {file_name}: {status}")
    except Exception as e:
        logger.error(f"Failed to update state_report.json: {e}")
        raise


# Specify the file path
structure= 'alignment_files/structure.json'

# Open the JSON file and load the structure
with open(structure, 'r') as json_file:
   structure= json.load(json_file)


# Define JSON Schemas
STRUCTURE_SCHEMA = structure

# Specify the file path
models= 'alignment_files/models.json'

# Open the JSON file and load the other_values
with open(models, 'r') as json_file:
    models= json.load(json_file)

MODELS_SCHEMA = models

# Specify the file path
other_values = 'alignment_files/other_values.json'

# Open the JSON file and load the other_values
with open(other_values, 'r') as json_file:
    other_values = json.load(json_file)

# Print the loaded data
print(other_values)

OTHER_VALUES_SCHEMA = other_values

def validate_json(data, schema, filename):
    """Validate JSON data against a schema."""
    logger.debug(f"Validating {filename} against schema")
    try:
        validate(instance=data, schema=schema)
        logger.info(f"{filename} validation passed.")
    except ValidationError as ve:
        logger.error(f"{filename} validation failed: {ve.message}")
        raise

def main():
    try:
        # Load game description
        logger.info("Starting project initialization")
        subject_description = load_subject()

        # Generate structure.json
        try:
            structure = generate_structure(subject_description)
            validate_json(structure, STRUCTURE_SCHEMA, 'structure.json')
            save_json(structure, 'structure.json')
            generate_state_report('structure.json', 'Success', 'structure.json generated and validated successfully.')
        except Exception as e:
            generate_state_report('structure.json', 'Failed', str(e))
            logger.error(f"Error generating structure.json: {e}")
            sys.exit(1)

        # Generate models.json
        try:
            models = generate_models(structure)
            validate_json(models, MODELS_SCHEMA, 'models.json')
            save_json(models, 'models.json')
            generate_state_report('models.json', 'Success', 'models.json generated and validated successfully.')
        except Exception as e:
            generate_state_report('models.json', 'Failed', str(e))
            logger.error(f"Error generating models.json: {e}")
            sys.exit(1)

        # Generate OtherValues.json
        try:
            other_values = generate_other_values(subject_description, structure, models)
            validate_json(other_values, OTHER_VALUES_SCHEMA, 'OtherValues.json')
            save_json(other_values, 'OtherValues.json')
            generate_state_report('OtherValues.json', 'Success', 'OtherValues.json generated and validated successfully.')
        except Exception as e:
            generate_state_report('OtherValues.json', 'Failed', str(e))
            logger.error(f"Error generating OtherValues.json: {e}")
            sys.exit(1)

    except Exception as e:
        logger.critical(f"Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
