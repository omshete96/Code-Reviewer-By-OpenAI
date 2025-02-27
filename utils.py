from typing import Dict, Any  # Added the required imports

def format_analysis_results(results: Dict[str, Any], file_path: str) -> str:
    """Format analysis results for display"""
    output = []
    
    output.append(f"\n=== Code Analysis Results for {file_path} ===\n")
    
    # Style Issues
    output.append("Style Issues:")
    if results['style_issues']:
        for issue in results['style_issues']:
            output.append(f"- {issue}")
    else:
        output.append("- No style issues found")
    output.append("")
    
    # Rest of the code remains the same...
    
    # Complexity Issues
    output.append("Complexity Issues:")
    if results['complexity_issues']:
        for issue in results['complexity_issues']:
            output.append(f"- {issue}")
    else:
        output.append("- No complexity issues found")
    output.append("")
    
    # AI Suggestions
    output.append("AI Suggestions:")
    if results['ai_suggestions']:
        for suggestion in results['ai_suggestions']:
            output.append(f"- {suggestion}")
    else:
        output.append("- No AI suggestions available")
    output.append("")
    
    # Formatting
    output.append("Formatting:")
    if results['formatting']['needs_formatting']:
        output.append("- Code needs formatting. Run with --fix to apply suggested formatting.")
    else:
        output.append("- Code formatting looks good")
    
    return "\n".join(output)