# Web Task Assistant

> A Python-based web task assistant powered by Google's Gemini AI that interprets tasks, extracts web information, and generates PDF reports.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Gemini](https://img.shields.io/badge/AI-Gemini-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- AI-Powered Task Interpretation using Gemini
- Smart Web Scraping with retry mechanisms
- Visual Reports with charts and images
- Robust error handling and fallback systems
- Dynamic chart generation (Bar, Pie, Line)

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/web-task-assistant.git
cd web-task-assistant

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Add your Google API key to .env file
```

## Usage

```bash
python web_task_assistant.py
```

Example tasks:
```
"Find the top 5 AI related headlines"
"Get the latest cryptocurrency prices"
"Summarize recent space exploration news"
```

## Project Structure

```
web-task-assistant/
├── web_task_assistant.py   # Main script
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Core Functions

- `interpret_task()` - Task analysis using Gemini AI
- `fetch_webpage()` - Web content retrieval with retries
- `extract_information()` - Smart data extraction
- `create_chart()` - Data visualization
- `save_results_to_file()` - PDF report generation

## Dependencies

- google-generativeai >= 0.3.0
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- reportlab >= 4.0.0
- Pillow >= 10.0.0
- matplotlib >= 3.7.0

## Limitations

- Text processing: 10,000 chars max
- Images per report: 3 max
- Requires internet connection
- API rate limits apply

## Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Roadmap

- [ ] Additional chart types
- [ ] Caching system
- [ ] Authentication support
- [ ] Enhanced error reporting
- [ ] Custom PDF templates
- [ ] Concurrent scraping