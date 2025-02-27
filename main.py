import asyncio
import argparse
from pathlib import Path
from code_parser import CodeParser
from analyzer import CodeAnalyzer
from utils import format_analysis_results
from config import SUPPORTED_EXTENSIONS

async def main():
    parser = argparse.ArgumentParser(description='AI-powered Code Reviewer')
    parser.add_argument('path', help='Path to file or directory to analyze')
    parser.add_argument('--fix', action='store_true', help='Apply suggested formatting fixes')
    args = parser.parse_args()
    
    code_parser = CodeParser()
    analyzer = CodeAnalyzer()
    
    path = Path(args.path)
    
    if path.is_file():
        files = [path]
    else:
        files = [f for f in path.rglob('*') if f.suffix in SUPPORTED_EXTENSIONS]
    
    for file_path in files:
        try:
            print(f"\nAnalyzing {file_path}...")
            
            # Read and parse code
            code = code_parser.read_file(str(file_path))
            
            # Analyze code
            analysis_results = await analyzer.analyze_code(code, str(file_path))
            
            # Display results
            print(format_analysis_results(analysis_results, str(file_path)))
            
            # Apply formatting if requested
            if args.fix and analysis_results['formatting']['needs_formatting']:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(analysis_results['formatting']['formatted_code'])
                print(f"\nFormatting applied to {file_path}")
                
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())