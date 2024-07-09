# RankRAG Data Collection App

This Streamlit application is designed to facilitate data collection for training the RankRAG model. It allows users to input questions, answers, and context passages, which are essential for building a high-quality dataset for retrieval-augmented generation (RAG) tasks in this paper: https://arxiv.org/html/2407.02485v1.

## Features

- **Home/Add Data**: Input and save questions, answers, and context passages for various task types.
- **View Data**: Review the collected data and upload it to a Google Sheet for further processing and analysis.
- **Google Sheets Integration**: Automatically update Google Sheets with the collected data using a Google Cloud service account.

## Getting Started

### Prerequisites

- Conda
- Python 3.7 or later

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/casualcomputer/rankRag-train-data.git
   cd rankRag-train-data
   ```

2. **Create a Conda environment**:

   ```bash
   conda env create -f conda_environment.yaml
   conda activate rankrag-env
   ```

3. **Set up Google Cloud service account (TO-BE-CONTINUED)**:

   - Create a service account on Google Cloud.
   - Download the JSON key file.
   - Set the environment variable `gcp_service_account` with the content of the JSON key file.

   Example using a `.env` file:

   ```bash
   echo 'gcp_service_account={"type": "service_account", "project_id": "...", ...}' > .env
   ```

4. **Run the application**:

   ```bash
   streamlit run app.py
   ```

### Usage

1. **Home/Add Data**:

   - Select a task type from the dropdown menu.
   - Enter the question, answer, and context passages.
   - Click the "Submit" button to save the data.

2. **View Data**:
   - Navigate to the "View Data" page using the sidebar.
   - Review the collected data for each task type.
   - Click the "Upload to Google Sheet" button to update the Google Sheet with the collected data.
