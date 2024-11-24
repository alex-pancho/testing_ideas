import re
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DoxygenComment:
    """Represents a parsed Doxygen comment"""
    brief: str
    description: Optional[str] = None
    params: List[Dict[str, str]] = None
    returns: Optional[Dict[str, str]] = None
    throws: List[str] = None
    example: Optional[str] = None
    api: Optional[Dict] = None
    version: Optional[str] = None
    author: Optional[str] = None

class DoxygenParser:
    """Parser for Doxygen comments in C++ files"""
    
    def __init__(self):
        # Regex patterns for different Doxygen tags
        self.patterns = {
            'brief': r'@brief\s+([^\n]+)',
            'description': r'@details\s+([^@]+)',
            'param': r'@param\s+(\w+)\s+([^@]+)',
            'returns': r'@returns?\s+([^@]+)',
            'throws': r'@throws\s+(\w+)\s+([^@]+)',
            'example': r'@example[^`]*```cpp\s*([^`]+)```',
            'version': r'@version\s+([^\n]+)',
            'author': r'@author\s+([^\n]+)',
            'api': r'@api\s*([^@]+)'
        }
        
        # Compile all regex patterns
        self.compiled_patterns = {
            key: re.compile(pattern, re.MULTILINE | re.DOTALL)
            for key, pattern in self.patterns.items()
        }

    def extract_comments(self, cpp_file: str) -> List[str]:
        """Extract Doxygen comments from C++ file"""
        with open(cpp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all Doxygen comments
        comment_pattern = r'/\*\*(.*?)\*/'
        comments = re.finditer(comment_pattern, content, re.MULTILINE | re.DOTALL)
        return [comment.group(1).strip() for comment in comments]

    def parse_comment(self, comment: str) -> DoxygenComment:
        """Parse a single Doxygen comment into structured data"""
        result = DoxygenComment(brief="")
        
        # Extract brief description
        brief_match = self.compiled_patterns['brief'].search(comment)
        if brief_match:
            result.brief = brief_match.group(1).strip()
            
        # Extract detailed description
        desc_match = self.compiled_patterns['description'].search(comment)
        if desc_match:
            result.description = desc_match.group(1).strip()
            
        # Extract parameters
        param_matches = self.compiled_patterns['param'].finditer(comment)
        if param_matches:
            result.params = [
                {'name': m.group(1), 'description': m.group(2).strip()}
                for m in param_matches
            ]
            
        # Extract return value
        returns_match = self.compiled_patterns['returns'].search(comment)
        if returns_match:
            result.returns = {'description': returns_match.group(1).strip()}
            
        # Extract throws
        throws_matches = self.compiled_patterns['throws'].finditer(comment)
        if throws_matches:
            result.throws = [
                {'exception': m.group(1), 'description': m.group(2).strip()}
                for m in throws_matches
            ]
            
        # Extract example
        example_match = self.compiled_patterns['example'].search(comment)
        if example_match:
            result.example = example_match.group(1).strip()
            
        # Extract version
        version_match = self.compiled_patterns['version'].search(comment)
        if version_match:
            result.version = version_match.group(1).strip()
            
        # Extract author
        author_match = self.compiled_patterns['author'].search(comment)
        if author_match:
            result.author = author_match.group(1).strip()
            
        # Extract API information
        api_match = self.compiled_patterns['api'].search(comment)
        if api_match:
            try:
                result.api = yaml.safe_load(api_match.group(1))
            except yaml.YAMLError:
                result.api = None
                
        return result

    def comment_to_yaml(self, comment: DoxygenComment) -> dict:
        """Convert parsed comment to YAML-compatible dictionary"""
        yaml_dict = {
            'brief': comment.brief
        }
        
        if comment.description:
            yaml_dict['description'] = comment.description
            
        if comment.params:
            yaml_dict['parameters'] = comment.params
            
        if comment.returns:
            yaml_dict['returns'] = comment.returns
            
        if comment.throws:
            yaml_dict['exceptions'] = comment.throws
            
        if comment.example:
            yaml_dict['example'] = comment.example
            
        if comment.version:
            yaml_dict['version'] = comment.version
            
        if comment.author:
            yaml_dict['author'] = comment.author
            
        if comment.api:
            yaml_dict['api'] = comment.api
            
        return yaml_dict

    def generate_yaml(self, cpp_file: str, output_file: str):
        """Generate YAML documentation from C++ file"""
        comments = self.extract_comments(cpp_file)
        parsed_comments = [self.parse_comment(comment) for comment in comments]
        
        documentation = {
            'file': Path(cpp_file).name,
            'elements': [
                self.comment_to_yaml(comment)
                for comment in parsed_comments
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(documentation, f, default_flow_style=False, allow_unicode=True)

def main():
    """Example usage of the parser"""
    parser = DoxygenParser()
    
    # Example usage with error handling
    try:
        parser.generate_yaml(
            cpp_file='account_manager.hpp',
            output_file='documentation.yaml'
        )
        print("Documentation generated successfully!")
        
    except FileNotFoundError:
        print("Error: Source C++ file not found!")
        
    except Exception as e:
        print(f"Error generating documentation: {str(e)}")

if __name__ == '__main__':
    import sys
    from pathlib import Path
    # Check number of args
    if len(sys.argv) < 3:
        print("Use: \npython3 doxygen_yaml_generator.py <input_file> <output_file>")
        sys.exit(1)

    # Get filenames from cmd
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"ERROR: {input_file} not found")
        sys.exit(1)

    # Call DoxygenParser with using filenames
    doxygen_parser = DoxygenParser()
    doxygen_parser.generate_yaml(str(input_file), str(output_file))