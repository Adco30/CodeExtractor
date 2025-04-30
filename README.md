# CodeExtractor

CodeExtractor is a lightweight PyQt5 desktop application that lets you navigate a workspace, select any project folder or individual file, filter by file extension, strip comments or imports, and export your source code as Markdown-ready fenced code blocks—all with live progress updates and customizable exclusions stored in a JSON config.

---

## Features

- **Workspace Browser**  
  Browse and select any directory; your last workspace path is remembered.  
- **File-Type Filters**  
  Choose which extensions to include via dynamic checkboxes per project.  
- **Options**  
  • Remove imports (Java)  
  • Remove comments (Python & C-like)  
  • Exclude directories or glob patterns  
- **Indented View**  
  Tree-view of files (with optional detailed class/function listings) and “Copy Treemap” to clipboard.  
- **Markdown Export**  
  Generates Markdown with `**path/to/file**` headers and triple-fenced code blocks, streamed in chunks with progress feedback.  
- **Persistence**  
  All settings, column widths, exclusions, and filter preferences are saved to `code_extractor_config.json`.

---

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Clone this repository:  
   ```bash
   git clone https://github.com/Adco30/CodeExtractor.git
   cd CodeExtractor

### Watch the YouTube demo:


[<img width="1425" alt="Screenshot 2025-04-30 at 12 06 11 AM 2" src="https://github.com/user-attachments/assets/6557f73e-f731-4957-8428-6299a2f4f5fb" />](https://youtu.be/nWZmAp8D0sM)
