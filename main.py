"""
Meeting-Notes-to-Actions Agent CLI

Command-line interface for the meeting notes agent.
"""

import argparse
import json
import sys
from pathlib import Path

from src.parser import MeetingNotesParser
from src.formatters import OutputFormatter


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Meeting-Notes-to-Actions Agent: Convert meeting notes into action items',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m meeting_agent --input notes.txt --format markdown
  python -m meeting_agent --input daily_standup.txt --output-dir results/ --format json,csv,markdown
  python -m meeting_agent --input notes.txt --format html --output report.html
        """
    )
    
    # Input options
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Input file with meeting notes'
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        help='Input directory with multiple meeting note files'
    )
    
    # Output options
    parser.add_argument(
        '--format', '-f',
        type=str,
        default='markdown',
        choices=['json', 'csv', 'markdown', 'html', 'dict'],
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file (if not specified, uses stdout)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory for multiple files'
    )
    
    # Configuration
    parser.add_argument(
        '--config',
        type=str,
        help='Configuration file (.yml)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.input and not args.input_dir:
        parser.error('Either --input or --input-dir must be specified')
    
    # Process input
    if args.input:
        process_file(args.input, args.format, args.output, args.verbose)
    elif args.input_dir:
        process_directory(args.input_dir, args.format, args.output_dir, args.verbose)


def process_file(input_file: str, output_format: str, output_file: str = None, verbose: bool = False):
    """
    Process a single meeting notes file.
    
    Args:
        input_file: Path to input file
        output_format: Output format (json, csv, markdown, html)
        output_file: Output file path (optional)
        verbose: Enable verbose output
    """
    # Read input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    if verbose:
        print(f"Reading: {input_file}")
    
    notes_text = input_path.read_text()
    
    # Parse meeting notes
    if verbose:
        print("Parsing meeting notes...")
    
    parser = MeetingNotesParser(notes_text)
    structured_data = parser.parse()
    
    if verbose:
        print(f"Extracted {len(structured_data['action_items'])} action items")
        print(f"Extracted {len(structured_data['decisions'])} decisions")
    
    # Format output
    formatter = OutputFormatter(structured_data)
    
    if output_format == 'json':
        output = formatter.to_json()
    elif output_format == 'csv':
        output = formatter.to_csv()
    elif output_format == 'html':
        output = formatter.to_html()
    elif output_format == 'dict':
        output = json.dumps(formatter.to_dict(), indent=2)
    else:  # markdown
        output = formatter.to_markdown()
    
    # Write output
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output)
        if verbose:
            print(f"Written to: {output_file}")
    else:
        print(output)


def process_directory(input_dir: str, output_format: str, output_dir: str = None, verbose: bool = False):
    """
    Process multiple meeting notes files in a directory.
    
    Args:
        input_dir: Path to input directory
        output_format: Output format
        output_dir: Output directory
        verbose: Enable verbose output
    """
    input_path = Path(input_dir)
    if not input_path.is_dir():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find all text files
    txt_files = list(input_path.glob('*.txt'))
    md_files = list(input_path.glob('*.md'))
    files = txt_files + md_files
    
    if not files:
        print(f"Error: No .txt or .md files found in {input_dir}", file=sys.stderr)
        sys.exit(1)
    
    if verbose:
        print(f"Found {len(files)} meeting note files")
    
    # Create output directory if needed
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Process each file
    for input_file in files:
        if verbose:
            print(f"\nProcessing: {input_file.name}")
        
        # Generate output filename
        stem = input_file.stem
        ext_map = {'json': '.json', 'csv': '.csv', 'markdown': '.md', 'html': '.html'}
        output_ext = ext_map.get(output_format, '.txt')
        
        if output_dir:
            output_file = str(Path(output_dir) / f"{stem}{output_ext}")
        else:
            output_file = None
        
        process_file(str(input_file), output_format, output_file, verbose=False)


if __name__ == '__main__':
    main()
