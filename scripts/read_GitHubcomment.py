# This script takes the comment from GitHub and split it into two yaml files.
# The first one is the new configuration yaml
# The second one is the new subsets configuration file
# Usage: python read_GitHubcomment.py --fileGitHub comment.tmp --fileSubset default_multi_subset.yaml

# use ruamel.yaml because it keeps the formatting 
# when using dump function
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.parser import ParserError
from ruamel.yaml.constructor import ConstructorError
yaml = YAML()
yaml.explicit_start = True
yaml.preserve_quotes = True  # Optional: preserve quoting style
yaml.strict = True  # be strict about syntax 
yaml.indent(mapping=4, sequence=6, offset=4)

import re

def update_configs(new_data, default_data):
    if 'parameters' in default_data and 'parameters' in new_data:
        default_params = default_data['parameters']
        override_params = new_data['parameters']
        
    # Add or update "parameters" in default config with the new ones
    for key, value in override_params.items():
        default_params[key] = value
    
    # Reorder keys to remove spacing issues
    new_params = CommentedMap()
    for key in list(default_params.keys()):
        new_params[key] = default_params[key]
        
    default_data['parameters'] = new_params
    
    # Merge header keys
    default_data["shortName"] = new_data.get("shortName")
    default_data["longName"] = new_data.get("longName", new_data.get("shortName"))
    default_data["description"] = new_data.get("description", "Configuration provided by user")
    
    # Write the new configurations into separated files
    filename = f"{new_data['shortName']}.yaml"
    with open(f"../HGCTPGValidation/config/{filename}", "w") as file:
        yaml.explicit_start = True
        yaml.dump(default_data, file)

def update_subsets(new_data, default_data, defaultSubsetFile):
    # Get the name of the new subset
    newSubsetName = new_data.get("subsetName")
    newSubsetDescription = new_data.get("description", "Configuration provided by user")
    # Get the new couple of subsets
    newSubset = new_data.get("configuration")
    
    # Read the subset configuration file as a string
    with open(f"../HGCTPGValidation/config/{defaultSubsetFile}", "r") as file:
        # Removes newlines and spaces to avoid problems when writing the new subset pairs
        subsetConfig = file.read().strip()
    
    # Get the configuration defined in default_multi_subset.yaml
    # and replace the subsetname and the description
    defaultConfig = yaml.load(subsetConfig)
    defaultConfig["subsetName"] = newSubsetName
    defaultConfig["description"] = newSubsetDescription
    
    # New file name
    filename = f"{new_data['subsetName'].replace(' ', '_')}.yaml"
    with open(f"../HGCTPGValidation/config/{filename}","w") as f:
        yaml.dump(defaultConfig, f)
        yaml.explicit_start = False # Needed in order to not use --- before the new set of configurations
        yaml.dump(newSubset, f)
    
    # The new subset name will overwrite the environment variable CONFIG_SUBSET
    return(newSubsetName)
    
def extract_yaml_block(comment):
    # Match text between ```yaml and ```
    match = re.search(r"```yaml\s*(.*?)\s*```", comment, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

def main(tmpFile, defaultSubsetFile):
    
    # Load the default.yaml
    with open(f"../HGCTPGValidation/config/default.yaml", "r") as file:
        default_data = yaml.load(file)
    
    # Read the comment from GitHub
    with open(f"../{tmpFile}", "r") as file:
        config = file.read()
    
    # Default subset name is used if there is no a new subset in the GitHub comment
    subsetName = "default_multi_subset"
    
    # Extract the yaml block from comment
    yaml_block = extract_yaml_block(config)
    if (yaml_block):
        # Split on '---' and filter out empty parts
        yaml_blocks = [part.strip() for part in yaml_block.split('---') if part.strip()]
        
        # Go through all parsed blocks
        try:
            parsed_blocks = [yaml.load(block) for block in yaml_blocks]
        except ScannerError as e:
            raise Exception(f"\n\n YAML ScannerError: likely caused by an invalid character or bad indentation in the PR comment. \n\n {e}")
        except ParserError as e:
            raise Exception(f"\n\n YAML ParserError: the configuration from the PR comment has a syntax issue (ex. different quotation marks). \n\n {e}")
        except ConstructorError as e:
            raise Exception(f"\n\n YAML ConstructorError: The YAML parser could not create a Python representation from the YAML element (scalar, list, mapping, or tagged object).\n\n {e}")
        except YAMLError as e:
            raise Exception(f"\n\n General YAML Error.\n\n {e}")
        except Exception as e:
            raise Exception(f"\n\n An unexpected error occurred while reading the PR comment. \n\n {e}")
        
        if len(parsed_blocks) >= 1:
            for block in parsed_blocks[0:]:
                if "shortName" in block: # process the new configurations
                    update_configs(block, default_data)
                elif "subsetName" in block: # process the subset configuration
                    subsetName = update_subsets(block, default_data, defaultSubsetFile)
                else:
                    raise Exception(f"\n\n The new configurations are not correct.\n Please check the spelling of the key words shortName and subsetName in the PR comment.\n\n")
    
    print(subsetName)

if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--fileGitHub', dest='fileGitHub', help=' ', default='')
    parser.add_option('--fileSubset', dest='fileSubset', help=' ', default='')
    (opt, args) = parser.parse_args()
    
    main(opt.fileGitHub, opt.fileSubset)

