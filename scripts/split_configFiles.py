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

def main(releaseName):
    print(releaseName)
    # Load the default.yaml
    with open(f"../HGCTPGValidation/config/{releaseName}.yaml", "r") as file:
        #configs = yaml.load(file)
        configs = file.read()
        
    # Split on '---' and filter out empty parts
    yaml_blocks = [part.strip() for part in configs.split('---') if part.strip()]
        
    # Go through all parsed blocks
    try:
        parsed_blocks = [yaml.load(block) for block in yaml_blocks]
    except Exception as e:
        raise Exception(f"\n\n An unexpected error occurred while reading the configurations. \n\n {e}")
    
    if len(parsed_blocks) >= 1:
        for block in parsed_blocks[0:]:
            # Write the new configurations into separated files
            filename = f"{block['shortName']}.yaml"
            print(filename)
            with open(f"../HGCTPGValidation/config/{filename}", "w") as file:
                yaml.explicit_start = True
                yaml.dump(block, file)
    
if __name__ == "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--releaseName', dest='releaseName', help=' ', default='')
    (opt, args) = parser.parse_args()
    
    main(opt.releaseName)
