
# Project Setup Instructions

Follow these steps to set up and run the project:

## Prerequisites
Ensure you have the following installed on your system:
- Python (>= 3.8)
- pip (Python package manager)

## Required Python Libraries
The project requires the following libraries:
- `matplotlib`
- `os`
- `pandas`
- `seaborn`
- `sklearn`

## Setting Up the Environment
1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install matplotlib pandas seaborn scikit-learn
   ```

## Running the Project
1. Make sure all necessary datasets and scripts are in their correct locations.
2. Run the `main.py` file:
   ```bash
   python main.py
   ```

The program will execute, process data, and generate outputs as described in the documentation.

## Notes
- Keep your `venv` folder within the project directory for convenience.
- If the `venv` folder is deleted, repeat the setup steps above to recreate it.
