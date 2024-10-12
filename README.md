# Code Complexity Analyzer

## Overview

The **Code Complexity Analyzer** is a web application designed to help developers analyze the complexity of their code. It provides insights into both time and space complexity, offering recommendations for code optimization. The application uses modern web technologies, including Flask, Chart.js, and Tailwind CSS.

## Features

- **Code Analysis**: Submit your code for analysis and receive feedback on its complexity.
- **Visualizations**: Visual representations of time and space complexity using Chart.js.
- **Optimized Code Suggestions**: Get suggestions for improving your code's efficiency.
- **Syntax Highlighting**: Enjoy syntax highlighting for code input with Prism.js.
- **Gemini Flash 1.5**: Leverages the Gemini Flash 1.5 model for advanced code analysis and optimization.

## Technologies Used

- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Backend**: Python, Flask
- **Data Visualization**: Chart.js
- **Code Highlighting**: Prism.js
- **Code Analysis Model**: Gemini Flash 1.5 (free version)

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/swarooppatilx/code-analyzer.git
   cd code-analyzer
```
2. **Creating a virtual environment**:
```bash
 # On Linux/MacOS
python3 -m venv venv
source venv/bin/activate 
 # On Windows:
 venv\Scripts\activate
```

3. **Install the required dependinces**:
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python3 app.py
```


## License

This project is licensed under the **GNU General Public License v3.0** (GPL v3).

**GPL v3** is a free, copyleft license for software. It guarantees end users the freedom to run, study, share, and modify the software. It also ensures that derivative works must also be licensed under the same terms, ensuring that the code remains open source. You can read more about the license [here](https://www.gnu.org/licenses/gpl-3.0.en.html).