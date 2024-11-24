# Improving Unit Testing Through Three Key Steps: Code Documentation, Documentation Generation and Using Generative Frameworks

## Introduction
Unit testing is a key stage in software development, allowing you to check the functionality of individual parts of the code and ensure its reliability and compliance with requirements. However, as practice shows, the testing process is often cumbersome and slow due to a lack of well-structured documentation and high requirements for the initial preparation of tests. This article proposes three steps to optimise the testing process: documenting the code, automatically generating documentation, and using generative frameworks to create tests. These methods can significantly reduce testing time, improve test quality, and ensure easy code maintenance in the future.

## Step 1: Documentation via Comments

### Importance of Documentation
Quality code documentation is the foundation for effective testing. It helps:
- Better understand the purpose of each component
- Clearly define expected behavior
- Simplify the test writing process

In addition, in the proposed approach, documenting via comments allows you to immediately test new functionality through the generation of test cases.

### Example of Code Documentation via comments

Exmple for Account Manager prototype, used Doxygen:

```cpp
/**
 * @class AccountManager
 * @brief Account management system
 * @version 2.0.0
 * @author Account Team
 * 
 * @details
 * API Endpoints:
 *   - `/api/v1/accounts`
 *   - `/api/v1/profiles`
 * 
 * Security:
 *   - Bearer Authentication
 *   - API Key
 */
class AccountManager {
public:
    /**
     * @brief Creates a new user account.
     * 
     * @param accountData Contains information required to create a user account.
     * @return AccountResult Object containing details of the created account.
     * 
     * @throws DuplicateAccountError If an account with the same username or email already exists.
     * @throws ValidationError If the input data is invalid.
     * 
     * @example
     * Example request:
     *   AccountData accountData;
     *   accountData.username = "john_doe";
     *   accountData.email = "john@example.com";
     * 
     * Example response:
     *   AccountResult result;
     *   result.accountId = "acc_789012";
     *   result.status = "active";
     *   result.created = "2024-03-14T12:00:00Z";
     *   result.is_locked = false;
     */
    AccountResult createAccount(const AccountData& accountData);
};

```

Exmple for Account Manager prototype, used yaml:

```cpp
/**
 * @class AccountManager
 * @brief Account management system
 * @version 2.0.0
 * @author Account Team
 * 
 * @details
 * API Endpoints:
 *   - `/api/v1/accounts`
 *   - `/api/v1/profiles`
 * 
 * Security:
 *   - Bearer Authentication
 *   - API Key
 */
class AccountManager {
public:
    /**
     * @description: Creates new user account
     * 
     * @params:
     *   lookingForAccountData:
     *     type: LookingForAccountData
     *     required: true
     *     fields:
     *       username:
     *         type: string
     *         required: true
     *         description: Unique username
     *       email:
     *         type: string
     *         required: true
     *         format: email
     * 
     * @returns:
     *   type: AccountResult
     *   fields:
     *     accountId: string
     *     status: string
     *     created: datetime
     *     is_locked: bool
     * 
     * @throws:
     *   - DuplicateAccountError
     *   - ValidationError
     * 
     * @example:
     *   request:
     *     username: "john_doe"
     *     email: "john@example.com"
     *   response:
     *     accountId: "acc_789012"
     *     status: "active"
     *     created: "2024-03-14T12:00:00Z"
     *     is_locked: false
     */
    AccountResult createAccount(const AccountData& accountData);
};
```

## Step 2: Documentation Generation

### 2.1. From Comments to YAML: First Documentation Stage


#### Automatic YAML Generation
```python
# doxygen_yaml_generator.py
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
    import Path
    # Check number of args
    if len(sys.argv) < 3:
        print("Use: \npython3 doxygen_yaml_generator.py <input_file> <output_file>")
        sys.exit(1)

    # Get filenames from cmd
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exist():
        print(f"ERROR: {input_file} not found")
        sys.exit(1)

    # Call DoxygenParser with using filenames
    doxygen_parser = DoxygenParser()
    doxygen_parser.generate_yaml(str(input_file), str(output_file))
```

How  we can youse it?
```bash
python3 doxygen_yaml_generator my_cpp_file.hpp output.yaml
```

### 2.2. Displaying YAML Documentation

#### HTML Generator


### 2.3. CI/CD Integration

#### GitHub Actions Workflow
```yaml
name: Generate Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyyaml jinja2 libclang
    
    - name: Generate documentation
      run: |
        python doc_generator.py
        python html_generator.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs
```

### 2.4. Best Practices
1. **Comment Structure**:
   - Use consistent formatting
   - Include all necessary metadata
   - Specify data types and constraints

2. **YAML Generation**:
   - Validate generated YAML
   - Maintain data structure
   - Handle special cases

3. **Display**:
   - Create user-friendly navigation
   - Add documentation search
   - Ensure responsive design

4. **Maintenance**:
   - Update documentation regularly
   - Verify example accuracy
   - Collect user feedback

## Step 3: Using Generative Frameworks

### Benefits of Generative Testing
- Automatic test case generation
- Edge case coverage
- Developer time savings

### Popular Frameworks
1. **C++**:
   - Catch2
   - RapidCheck
   - GoogleTest with property-based testing

2. **Modern Frameworks**:
   - Hypothesis for Python
   - fast-check for JavaScript

### Example Using Hypothesis
```cpp
#include <rapidcheck.h>

rc::check("User creation with valid data", [](const std::string& username, 
                                            const std::string& email) {
    // Precondition: username and email must be valid
    RC_PRE(username.length() >= 3 && username.length() <= 50);
    RC_PRE(email.find('@') != std::string::npos);
    
    AccountManager manager;
    AccountData data{username, email};
    
    AccountResult result = manager.createAccount(data);
    
    RC_ASSERT(!result.accountId.empty());
    RC_ASSERT(result.status == "active");
});
```

## Conclusions
Implementing these three steps will help:
1. Improve code quality through clear documentation
2. Simplify project maintenance with automatically generated documentation
3. Increase test coverage using generative frameworks

## Implementation Recommendations
- Start small: document new components
- Set up automatic documentation generation in CI/CD
- Gradually add generative tests for critical components

## Useful Links
- [Doxygen Documentation](https://www.doxygen.nl/)
- [RapidCheck Documentation](https://github.com/emil-e/rapidcheck)
- [Catch2 Documentation](https://github.com/catchorg/Catch2)
