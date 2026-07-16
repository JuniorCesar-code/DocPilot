# DocPilot — Requirements Document

## Project description
A web application that automatically generates Python docstrings
using AI. The developer uploads a Python file, selects a 
documentation style, and receives generated docstrings for 
every function — without writing any documentation manually.

---

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | User can upload a Python (.py) file |
| FR2 | System extracts all functions automatically |
| FR3 | System identifies function names and parameters |
| FR4 | User selects documentation style (Google, NumPy, Sphinx) |
| FR5 | System generates a docstring per function using LLM |
| FR6 | User sees original function and docstring side by side |
| FR7 | User gives feedback to improve a docstring |
| FR8 | User downloads the documented file |

---

## Non-Functional Requirements

| ID | Type | Requirement | How we implemented it |
|----|------|-------------|----------------------|
| NFR1 | Security | API key never in code | Stored in .env file |
| NFR2 | Reliability | Handle wrong inputs | Error handling in /upload |
| NFR3 | Usability | Simple 3-step flow | Upload → Review → Export |
| NFR4 | Performance | Response under 10 seconds | claude-sonnet-4-6 model |
| NFR5 | Compatibility | Works in any browser | Plain HTML, no framework |

---

## Use Cases

### UC1 — Upload Python File
- **Actor:** Developer
- **Trigger:** User clicks "Upload and analyse"
- **Steps:**
  1. User selects .py file
  2. User selects style
  3. System validates file → main.py /upload endpoint
  4. System extracts functions → ast.parse()
  5. System returns function list as JSON
- **Result:** Functions displayed as clickable list
- **Errors handled:**
  - Wrong file type → "Please upload a Python file"
  - Empty file → "The file is empty"
  - No functions → "No functions found"

### UC2 — Generate Docstring
- **Actor:** Developer
- **Trigger:** User clicks a function in the list
- **Steps:**
  1. Frontend sends function to /generate endpoint
  2. main.py calls generate_docstring() in llm.py
  3. llm.py sends prompt to Anthropic API
  4. LLM returns docstring
  5. Frontend displays side by side
- **Result:** Docstring appears next to original function

### UC3 — Improve Docstring with Feedback
- **Actor:** Developer
- **Trigger:** User clicks "Improve it"
- **Steps:**
  1. User writes what should change
  2. Frontend sends feedback + original docstring to /generate
  3. LLM generates improved version
  4. New docstring displayed
- **Result:** Improved docstring shown

### UC4 — Export Documentation
- **Actor:** Developer
- **Trigger:** User clicks "Download"
- **Steps:**
  1. System inserts docstrings into original file
  2. File downloads automatically
- **Result:** Complete documented .py file downloaded

---

## Prompting Guide — how we used AI for requirements

We used the following prompt structure to generate and refine
our requirements (following the VL10 prompting guide):

**Context:**
"I am building a web application called DocGen that automatically
generates Python docstrings using AI."

**Task:**
"Generate functional and non-functional requirements and use cases."

**Output format:**
"Structured list with clear categories and IDs."

This prompt follows the three rules from VL10:
1. Context → what the system is
2. Clear task → what we want generated
3. Output format → how we want it structured