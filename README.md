<br>
<div align="center">
   <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2F4d36bc052c4340f997dd61eb19c1c64b">
      <img width="400" alt="AI Shell logo" src="https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2F1a718d297d644fce90f33e93b7e4061f">
    </picture>
</div>

<p align="center">
   An Python AI agent that writes and fixes code for you.
</p>

<p align="center">
   <a href="https://www.npmjs.com/package/@builder.io/micro-agent"><img src="https://img.shields.io/npm/v/@builder.io/micro-agent" alt="Current version"></a>
</p>
<br>

![Demo](https://cdn.builder.io/api/v1/file/assets%2FYJIGb4i01jvw0SRdL5Bt%2F3306a1cff57b4be69df65492a72ae8e5)

# Micro Agent

Point Micro Agent at a file and a test (or screenshot), and it will write code for you until your tests pass or it more closely matches your design screenshot.
# Python Capabilities in Micro Agent

## Introduction

Micro Agent now supports Python, expanding its capabilities to include Python code generation, fixing, and optimization. This guide provides comprehensive instructions and examples for leveraging these new Python capabilities.

## Installation

Before you can use the Python capabilities, ensure you have Python installed on your system. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

This command installs all the necessary Python packages to get you started with Micro Agent's Python features.

## Usage Examples

### Example 1: Generating Python Code

To generate Python code, use the following command:

```bash
micro-agent generate-python "description of the Python code you want to generate"
```

This command prompts Micro Agent to generate Python code based on your description.

### Example 2: Fixing Python Code

If you have Python code that needs fixing or optimization, use:

```bash
micro-agent fix-python ./path/to/your/python_script.py
```

Micro Agent will analyze the script and attempt to fix any errors or inefficiencies.

### Example 3: Running Python Code

To execute Python code and see the output, use:

```bash
micro-agent run-python ./path/to/your/python_script.py
```

This command runs the specified Python script and displays the output.

## Advanced Usage

Micro Agent's Python capabilities also support more advanced features, such as code refactoring and performance optimization. For detailed information on these advanced features, refer to the official documentation.

## Conclusion

Micro Agent's Python capabilities offer a powerful toolset for Python developers, simplifying the process of code generation, fixing, and optimization. By following the instructions and examples provided in this guide, you can start leveraging these capabilities in your Python projects.
