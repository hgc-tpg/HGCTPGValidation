# This script takes the comment from GitHub and split it into two yaml files.
# The first one is the new configuration yaml
# The second one is the new subsets configuration file
# Usage: python read_GitHubcomment.py --fileGitHub comment.tmp --fileSubset default_multi_subset.yaml

# same code as read_GitHubcomment_5bis.py but create two function for managing config and subsets
# use ruamel.yaml because it keeps the formatting 
# when using dump function
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
yaml = YAML()
yaml.explicit_start = True
yaml.preserve_quotes = True  # Optional: preserve quoting style
yaml.indent(mapping=4, sequence=6, offset=4)
    
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
    
    # Merge top-level keys (optional)
    for key in ["shortName", "longName", "description"]:
        if key in new_data:
            default_data[key] = new_data[key]
    
    # Write the new configurations into separated files
    filename = f"{new_data['shortName']}.yaml"
    with open(f"../HGCTPGValidation/config/{filename}", "w") as file:
        yaml.explicit_start = True
        yaml.dump(default_data, file)

def update_subsets(new_data, default_data, defaultSubsetFile):
    # Get the name of the new subset
    newSubsetName = new_data.get("subsetName")
    newSubsetDescription = new_data.get("description")
    # Get the new couple of subsets
    newSubset = new_data.get("configuration")
            
    # Get the configuration defined in default_multi_subset.yaml
    # and replace the subsetname and the description
    with open(f"../HGCTPGValidation/config/{defaultSubsetFile}", "r") as file:
        defaultConfig = yaml.load(file)
        defaultConfig["subsetName"] = newSubsetName
        defaultConfig["description"] = newSubsetDescription
             
    # New file name
    filename = f"{new_data['subsetName'].replace(' ', '_')}.yaml"
    with open(f"../HGCTPGValidation/config/{filename}","w") as f:
        yaml.dump(defaultConfig, f)
        yaml.explicit_start = False # Needed in order to not use --- before the new set of configurations
        yaml.dump(newSubset, f)
    
    # Printing the new subset name will overwrite the environment variable CONFIG_SUBSET
    print(newSubsetName)
    
def main(tmpFile, defaultSubsetFile):

    # Load the default.yaml
    with open(f"../HGCTPGValidation/config/default.yaml", "r") as file:
        default_data = yaml.load(file)
    
    # Read the comment from GitHub
    with open(f"../{tmpFile}", "r") as file:
        config = file.read()
    # Remove the ``` at the end of the string
    fc=config.strip("\n```")
    
    # Split on '---' and filter out empty parts
    yaml_blocks = [part.strip() for part in fc.split('---') if part.strip()]
    
    # Go through all parsed blocks
    parsed_blocks = [yaml.load(block) for block in yaml_blocks]
    for block in parsed_blocks[1:]: # Skip the first block that do not contain configuration 
        if "shortName" in block: # process the new configurations
            update_configs(block, default_data)
        elif "subsetName" in block: # process the subset configuration
            update_subsets(block, default_data, defaultSubsetFile)
        else:
            print("default_multi_subset.yaml")

if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--fileGitHub', dest='fileGitHub', help=' ', default='')
    parser.add_option('--fileSubset', dest='fileSubset', help=' ', default='')
    (opt, args) = parser.parse_args()
    
    main(opt.fileGitHub, opt.fileSubset)

