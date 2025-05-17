from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
import json
import re
import argparse
import sys
from dotenv import load_dotenv
from prompts import format_input_prompt, format_analysis_prompt, format_report_prompt
from docx_converter import json_to_docx

def generate_report(query, output_file=None):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    model_id = "gemini-2.0-flash"
    google_search_tool = Tool(
        google_search = GoogleSearch()
    )
    
    print(f"Starting research on: {query}")
    print("Step 1/3: Generating search prompt...")
    input_response = client.models.generate_content(
        model=model_id,
        contents=format_input_prompt(query),
    )

    print("Step 2/3: Performing web search and gathering data...")
    research_response = client.models.generate_content(
        model=model_id,
        contents=input_response.text,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )

    print("Step 3/3: Analyzing data and preparing report...")
    analysis_response = client.models.generate_content(
        model=model_id,
        contents=format_analysis_prompt(research_response.text),
    )

    print("Finalizing report structure...")
    report_response = client.models.generate_content(
        model=model_id,
        contents=format_report_prompt(analysis_response.text),
    )

    try:
        json_text = report_response.text
        json_text = re.sub(r'^```json\s*', '', json_text)
        json_text = re.sub(r'\s*```$', '', json_text)
        
        report_json = json.loads(json_text)
        
        if output_file is None:
            words = query.split()[:4]
            base_name = "_".join(words).lower()
            base_name = re.sub(r'[^\w\s-]', '', base_name).strip()
            base_name = re.sub(r'[-\s]+', '_', base_name)
            output_file = f"{base_name}_report.docx"
        
        output_doc = json_to_docx(report_json, output_file)
        print(f"Report generated: {output_doc}")
        return output_doc
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Generate a business intelligence report on any topic or industry'
    )
    parser.add_argument(
        'query', 
        type=str, 
        nargs='?', 
        help='Business query to research (e.g., "Who are the key players in the cloud computing industry?")'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output filename for the Word document (default: based on query)'
    )
    parser.add_argument(
        '--example',
        action='store_true',
        help='Use default example query about esports industry'
    )
    
    args = parser.parse_args()
    
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
        print("Create a .env file with the following content: GOOGLE_API_KEY=your_api_key_here")
        sys.exit(1)
    
    if args.query:
        high_level_query = args.query
    elif args.example:
        high_level_query = "What are the key players in the Esports Industry?"
        print(f"Using example query: \"{high_level_query}\"")
    else:
        print("No query provided. Please enter your business query below:")
        high_level_query = input("> ")
        
        if not high_level_query.strip():
            print("No query entered. Using default example query.")
            high_level_query = "What are the key players in the Esports Industry?"
    
    generate_report(high_level_query, args.output)

if __name__ == "__main__":
    main()