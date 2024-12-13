# Polynomial Arithmetic in GF(2^m)

This project provides Python implementations for performing arithmetic operations on polynomials in **GF(2^m)**, where \( 2 \leq m \leq 8 \). It supports a comprehensive range of polynomial operations based on predefined irreducible polynomials. Additionally, the project offers both an **offline desktop version** and an **online Flask-based web application** with AI integration to assist users in understanding the computation results.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Offline Version (Desktop Application)](#offline-version-desktop-application)
  - [Online Version (Web Application)](#online-version-web-application)
- [Running the Applications](#running-the-applications)
  - [Offline Version](#offline-version)
  - [Online Version](#online-version)
- [Usage](#usage)
  - [Offline Version](#offline-version-1)
  - [Online Version](#online-version-1)
- [AI Integration](#ai-integration)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

---

## Features

The application supports the following operations in **GF(2^m)**:

1. **Modulo Reduction**
2. **Finding the Inverse**
3. **Addition**
4. **Subtraction**
5. **Multiplication**
6. **Division**
7. **AI Integration**: Provides step-by-step explanations of operations to help users understand the results.

---

## Prerequisites

- **Python 3.6+**: Ensure Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).
- **Virtual Environment (Recommended)**: It's advisable to use a virtual environment to manage dependencies.

---

## Installation

### Offline Version (Desktop Application)

This version uses **Tkinter** for the GUI and requires the `ttkbootstrap` library.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/polynomial-arithmetic-gf2m.git
   cd polynomial-arithmetic-gf2m
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment**

   - **Windows:**
     ```bash
     env\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source env/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Online Version (Web Application)

This version uses Flask for the web framework and integrates with OpenAI's GPT-4 for AI-driven explanations.

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/polynomial-arithmetic-gf2m.git
   cd polynomial-arithmetic-gf2m
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment**

   - **Windows:**
     ```bash
     env\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source env/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**

   - Set the OpenAI API key for AI integration:
     - **Windows:**
       ```bash
       set OPENAI_API_KEY=your-openai-api-key
       ```
     - **macOS/Linux:**
       ```bash
       export OPENAI_API_KEY='your-openai-api-key'
       ```

   Replace `your-openai-api-key` with your actual OpenAI API key.

---

## Running the Applications

### Offline Version

1. **Navigate to the Project Directory**

   ```bash
   cd polynomial-arithmetic-gf2m
   ```

2. **Activate the Virtual Environment**

   - **Windows:**
     ```bash
     env\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source env/bin/activate
     ```

3. **Run the Application**

   ```bash
   python app.py
   ```

   This will launch the desktop application using Tkinter, allowing you to perform polynomial arithmetic operations locally.

### Online Version

1. **Navigate to the Project Directory**

   ```bash
   cd polynomial-arithmetic-gf2m
   ```

2. **Activate the Virtual Environment**

   - **Windows:**
     ```bash
     env\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source env/bin/activate
     ```

3. **Set Environment Variables**

   Ensure the `OPENAI_API_KEY` is set as described in the [Installation](#installation) section.

4. **Run the Flask Application**

   ```bash
   python appflask.py
   ```

   Open your browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the web application.

---

## Usage

### Offline Version

- Launch the desktop application.
- Use the GUI to input polynomials and select desired operations.

### Online Version

- Open the web application in your browser.
- Enter the polynomials and operations in the provided fields.

---

## AI Integration

The online version integrates with OpenAI's GPT-4 to:
- Explain the steps of polynomial arithmetic.
- Provide insights into the results for better understanding.

---

## Project Structure

```
polynomial-arithmetic-gf2m/
├── app.py                 # Offline version entry point
├── appflask.py            # Online version entry point
├── requirements.txt       # Dependencies
├── static/                # Static files (CSS, JS, etc.)
├── templates/             # HTML templates for the web application
├── utils/                 # Utility modules for polynomial operations
└── README.md              # Project documentation
```

---

## Dependencies

- **Tkinter**
- **Flask**
- **ttkbootstrap**
- **OpenAI API**

Install all dependencies using:

```bash
pip install -r requirements.txt
```



## Acknowledgements

- OpenAI for GPT-4 integration.
- Python community for providing robust libraries.

