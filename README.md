
---

# 🌐 Intelligent_Web_Agent

> 🔍 A Python-based intelligent assistant powered by **Gemini AI** that interprets natural language tasks, scrapes the web, visualizes data, and generates polished PDF reports.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](../../issues)

---

## 🚀 Features

- 🤖 **AI-Powered Task Interpretation** using Google’s **Gemini**
- 🌐 **Smart Web Scraping** with robust retry and fallback
- 📊 **Visual Insights** via dynamic charts (Bar, Pie, Line)
- 🧠 **Information Extraction** from live web pages
- 🖼️ **Media-Aware Reporting** with chart and image support
- 📄 **Polished PDF Report** generation with visuals and summaries
- 🔒 **Robust Error Handling** to gracefully manage failures

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/intelligent_web_agent.git
cd intelligent_web_agent

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Add your Gemini API key to .env file
```

---

## 🧠 How It Works

1. **Input a Natural Language Task**
2. **Gemini AI** interprets the intent
3. Web scraping fetches relevant live content
4. Extracted data is summarized and visualized
5. A final PDF report is generated 📄

---

## 🛠️ Usage

```bash
python intelligent_web_agent.py
```

Example prompts:
- `"Find the top 5 AI-related headlines"`
- `"Get the latest cryptocurrency prices"`
- `"Summarize recent space exploration news"`

---

## 📁 Project Structure

```
intelligent_web_agent/
├── intelligent_web_agent.py   # Main script
├── requirements.txt        # Python dependencies
├── .env.example            # Env template
└── README.md               # Project documentation
```

---

## 🧩 Core Functions

| Function | Description |
|----------|-------------|
| `interpret_task()` | Uses Gemini to parse and understand the task |
| `fetch_webpage()` | Retrieves relevant content from the web with retry logic |
| `extract_information()` | Extracts structured data from unstructured text |
| `create_chart()` | Generates charts using `matplotlib` |
| `save_results_to_file()` | Compiles everything into a PDF using `reportlab` |

---

## 📚 Dependencies

- `google-generativeai >= 0.3.0`
- `requests >= 2.31.0`
- `beautifulsoup4 >= 4.12.0`
- `reportlab >= 4.0.0`
- `Pillow >= 10.0.0`
- `matplotlib >= 3.7.0`

Install them using:

```bash
pip install -r requirements.txt
```

---

## ⚠️ Limitations

- Max text length: **10,000 characters**
- Max images per report: **3**
- Internet connection required 🌐
- Subject to **Gemini API rate limits**

---

## 🌱 Contributing

We welcome your ideas and improvements!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m "Add YourFeature"`
4. Push to GitHub: `git push origin feature/YourFeature`
5. Open a Pull Request ✅

---

## 🔭 Roadmap

- [ ] 📈 Support for more chart types (e.g., scatter, histogram)
- [ ] 🧰 Caching for repeated queries
- [ ] 🔐 API Authentication layer
- [ ] 🚨 Enhanced logging and error reporting
- [ ] 🎨 Custom PDF themes and templates
- [ ] ⚡ Async/concurrent scraping for speed boost

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---
