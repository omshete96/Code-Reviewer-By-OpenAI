import os
import ast
from typing import Dict, Any

class CodeParser:
    def __init__(self):
        self.supported_extensions = {'.py', '.js', '.java', '.cpp', '.ts'}

    def read_file(self, file_path: str) -> str:
        """Read code file and return its content"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def parse_python_code(self, code: str) -> Dict[str, Any]:
        """Parse Python code and extract relevant information"""
        try:
            tree = ast.parse(code)
            
            # Extract basic metrics
            metrics = {
                'functions': [],
                'classes': [],
                'imports': [],
                'line_count': len(code.splitlines()),
                'comment_count': len([line for line in code.splitlines() if line.strip().startswith('#')])
            }
            
            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics['functions'].append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'line_number': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    metrics['classes'].append({
                        'name': node.name,
                        'line_number': node.lineno
                    })
                elif isinstance(node, ast.Import):
                    metrics['imports'].extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    metrics['imports'].append(f"{node.module}")
            
            return metrics
            
        except SyntaxError as e:
            return {'error': f"Syntax error in code: {str(e)}"}