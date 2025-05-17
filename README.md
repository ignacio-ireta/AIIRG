# Business Intelligence Report Generator

Generate professional business reports on any industry using Google's Gemini API.

## Setup

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

Generate a report with a command-line query:
```
python main.py "Who are the key players in the cloud computing industry?"
```

Use the example query about esports:
```
python main.py --example
```

Run without arguments for interactive prompt:
```
python main.py
```

## Options

```
usage: main.py [-h] [-o OUTPUT] [--example] [query]

positional arguments:
  query                 Business query to research

options:
  -h, --help            show help message
  -o OUTPUT, --output OUTPUT
                        Output filename for the Word document
  --example             Use example query about esports industry
```

## Components

- `main.py` - Main script that handles queries and generates reports
- `prompts.py` - Stores prompts for LLM interactions
- `docx_converter.py` - Converts JSON data to Word documents
- `requirements.txt` - Required Python packages

## Report Structure

Generated reports include:
- Executive Summary
- Key Trends
- Competitive Landscape
- Insights
- Recommendations
- Limitations

## Requirements

- Python 3.6+
- Google API key with Gemini and Search access 