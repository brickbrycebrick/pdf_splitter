# PDF Chapter Splitter

A Python tool to split PDF files into chapters or sections automatically.

## Description

This tool takes a PDF file as input and splits it into separate PDF files based on chapter or section markers. It's particularly useful for breaking down large academic books or documents into more manageable pieces.

## Requirements

- Python 3.x
- Required packages (install via pip):
  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. Place your PDF file in the `books` directory
2. Run the script:
   ```python
   python run.py
   ```
3. Split PDF files will be created in the `output` directory

## Configuration

In `run.py`, you can configure:
- `input_pdf`: Path to your input PDF file
- `output_dir`: Directory where split PDFs will be saved
- `debug`: Set to True for detailed output

