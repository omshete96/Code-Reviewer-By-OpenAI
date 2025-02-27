from openai import OpenAI
from typing import Dict, List, Any
import black
from radon.complexity import cc_visit
from config import OPENAI_API_KEY, MAX_LINE_LENGTH, COMPLEXITY_THRESHOLD

class CodeAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    async def analyze_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """Analyze code and return suggestions"""
        analysis_results = {
            'style_issues': self._check_style(code),
            'complexity_issues': self._check_complexity(code),
            'ai_suggestions': await self._get_ai_suggestions(code),
            'formatting': self._check_formatting(code)
        }
        return analysis_results
    
    def _check_style(self, code: str) -> List[str]:
        """Check code style issues"""
        issues = []
        
        # Check line length
        for i, line in enumerate(code.splitlines(), 1):
            if len(line) > MAX_LINE_LENGTH:
                issues.append(f"Line {i} is too long ({len(line)} > {MAX_LINE_LENGTH} characters)")
        
        # Check empty lines between functions
        lines = code.splitlines()
        for i in range(1, len(lines)):
            if lines[i].startswith(('def ', 'class ')) and lines[i-1].strip() != '':
                issues.append(f"Missing empty line before function/class definition at line {i+1}")
        
        return issues
    
    def _check_complexity(self, code: str) -> List[str]:
        """Check code complexity using radon"""
        issues = []
        
        try:
            complexity_blocks = cc_visit(code)
            for block in complexity_blocks:
                if block.complexity > COMPLEXITY_THRESHOLD:
                    issues.append(
                        f"High complexity ({block.complexity}) in {block.name} at line {block.lineno}"
                    )
        except:
            issues.append("Unable to analyze code complexity")
        
        return issues
    
    async def _get_ai_suggestions(self, code: str) -> List[str]:
        """Get AI-powered code suggestions using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code review expert. Analyze the following code and provide specific, actionable improvements. Focus on code quality, readability, and best practices."
                    },
                    {
                        "role": "user",
                        "content": f"Please review this code and suggest improvements:\n\n{code}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract suggestions from the response
            suggestions = response.choices[0].message.content.split('\n')
            return [s for s in suggestions if s.strip()]
            
        except Exception as e:
            return [f"Error getting AI suggestions: {str(e)}"]
    
    def _check_formatting(self, code: str) -> Dict[str, Any]:
        """Check and suggest code formatting improvements"""
        try:
            formatted_code = black.format_str(code, mode=black.FileMode())
            needs_formatting = formatted_code != code
            
            return {
                'needs_formatting': needs_formatting,
                'formatted_code': formatted_code if needs_formatting else None
            }
        except Exception as e:
            return {
                'needs_formatting': False,
                'formatted_code': None,
                'error': f'Unable to format code: {str(e)}'
            }