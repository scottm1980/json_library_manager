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
            if 'subject' not in subject:
                logger.error("subject key not found in subject.json.")
                raise KeyError("subject key not found in subject.json.")
            logger.info("Loaded subject description.")
            return subject['subject']
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding {file_path}: {e}")
            raise

def save_json(data, filename):
    """Save a dictionary as a JSON file in the alignment_files folder."""
    folder = Path("alignment_files")
    folder.mkdir(exist_ok=True)  # Create folder if it doesn't exist
    file_path = folder / filename
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved {file_path}")
    except Exception as e:
        logger.error(f"Failed to save {file_path}: {e}")
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

def generate_structure(subject):
    """Generate structure.json using OpenAI."""
    logger.debug("Generating structure.json using OpenAI")
    prompt = f"""
Analyze the following game description and provide a complete file structure in JSON format. Include the necessary files, directories, and their relationships.

Description:
{subject}

**Do not include any code block delimiters. Provide only the JSON content.**
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "system",
                "content": (
                    "I am tasked with defining and then mapping out the typical contents of 'app/lib' folder in a Flutter Dart codebase but tailored to precisley reflect a SSoT code base."
                    " I will begin by visualizing the file structure that represents the app's folder hierarchy and the files within each folder."
                ),
                },
                {
            "role": "system",
            "content": (
                " I will first create an accurate mapping, allowing for and keeping all files in clean 'layers'."
                " I will translate the file structure into a JSON format that is a full and complete folder hierarchy and the files within each folder."
                " I will provide an optimized but complete file structure."
                " I will include these 'baseline' files & folders by default, alongside the files & folders for the specific app requirements:"
                " 'lib/appLifeCycleBloc(bloc,events,states)', 'lib/authBloc(bloc,events,states)', 'lib/navBloc(bloc,events,states)', 'lib/profileCubit(cubit, states)', 'lib/data', 'lib/services', 'lib/screens', 'lib/widgets', 'lib/helpers', 'lib/utils'."
                       ),
                },
                {"role": "user", "content": prompt}
            ],
            temperature=1.35,
            max_tokens=10000
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
    subject = load_subject()
    prompt = ("Analyze the subject and structure provided and then define all the required models. I require a model for all code and files across my codebase.")
          
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    { "role": "system", "content": ( "I am tasked with defining and mapping an entire DART 'model' set. This is required to produce a high fidelity app given a 'subject' and the finalized 'file structure'."
                                                    " I will begin by identifying the files in the 'file structure' that will require a model. I will then analyze the code, their relationships within the application, and define the 'model' required." "" ) }, 
                    { "role": "system", "content": ( " I will first create an accurate mapping, allowing for and keeping all models in clean 'layers'." 
                                                    " I will provide an optimized and complete definition of all required 'models'. I will reuse models where possible, such as usermodel serving both profile and auth." " I will always include 'baseline models' by default alongside the app subject-specific models. For instance, usermodel can be considered a baseline model." ) },
                    {"role": "assistant", "content": f"{subject}"}, 
                    {"role": "assistant", "content": f"{json.dumps(structure_json, indent=4)}"},
                    {"role": "user", "content": f"{prompt}"}
            ],
            temperature=1.35,
            max_tokens=5000
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
    """Generate other_values.json using OpenAI."""
    logger.debug("Generating other_values.json using OpenAI")
    prompt = f"""
Based on the following subject, structure, and models, generate a JSON file containing predefined events, states, function signatures, and other reusable values.

Subject:
{json.dumps({"subject": subject_json}, indent=4)}

Structure:
{json.dumps(structure_json, indent=4)}

Models:
{json.dumps(models_json, indent=4)}

**Do not include any code block delimiters. Provide only the JSON content.**
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    {
                    "role": "system",
                    "content": (
                        "I am tasked with defining non-model values used throughout a Flutter Dart application."
                        " I will utilize three different input JSONs: subject, file_structure, and models, to derive these values."
                    ),
                },
                {
                    "role": "system",
                    "content": (
                        "I will create an accurate representation of these non-model values, which include app-wide constants, settings, and reusable parameters."
                        " I will translate these values into a JSON format that consolidates key information derived from subject, file_structure, and models."
                        " I will provide an optimized but complete definition of all non-model values."
                        " These values may include default settings, predefined events, reusable utility constants, app states, and other relevant configurations."
                    ),
                },
                {
                    "role": "assistant",
                    "content": 
                        "event_names"
                        "state_names"
                        "function_names"
                        "inputs_outputs"
                        "imported_packages"
                        "imported_classes"
                        "widget_names"
                        "variable_names"
                        "constant_names"
                        "class_names"
                        "mixin_names"
                        "enum_names"
                        "method_names"
                        "data_types"
                        "annotations"
                        "inherited_classes"
                        "global_variables"
                        "final_variables"
                        "library_names"
                        "documentation_comments"
                        "file_names"
                        "file_locations"
                        "used_themes"
                        "event_listeners"
                        "dependencies"
                        "route_names"
                        "color_definitions"
                        "configuration_files"
                    
                },
                {"role": "user", "content": prompt}
            ],
            temperature=1.35,
            max_tokens=5000
        )
        raw_content = response.choices[0].message.content.strip()
        cleaned_content = extract_json(raw_content)
        other_values = json.loads(cleaned_content)
        logger.info("Generated other_values.json successfully.")
        return other_values
    except Exception as e:
        logger.error(f"Error generating other_values.json: {e}")
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
        subject = load_subject()

        # Generate structure.json
        try:
            structure = generate_structure(subject)
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

        # Generate other_values.json
        try:
            other_values = generate_other_values(subject, structure, models)
            validate_json(other_values, OTHER_VALUES_SCHEMA, 'other_values.json')
            save_json(other_values, 'other_values.json')
            generate_state_report('other_values.json', 'Success', 'other_values.json generated and validated successfully.')
        except Exception as e:
            generate_state_report('other_values.json', 'Failed', str(e))
            logger.error(f"Error generating other_values.json: {e}")
            sys.exit(1)

    except Exception as e:
        logger.critical(f"Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
