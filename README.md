# Knowledge Base Assistant App

## Overview

The **Knowledge Base Assistant App** allows users to create knowledge bases by uploading PDF files and querying them using a chatbot interface. Powered by OpenAI, this app enables you to create, manage, and interact with documents using natural language queries.

## Features

- **OpenAI Integration**: Interact with a chatbot using your OpenAI API key.
- **Knowledge Base Management**: Create new knowledge bases (vector stores) and manage existing ones.
- **Document Upload**: Upload PDF files to populate the knowledge base.
- **Chat Interface**: Ask questions based on the content of the uploaded documents.
  
## Prerequisites

- Python 3.x
- OpenAI API Key (You can get one [here](https://platform.openai.com/account/api-keys))
  
## Installation

1. Install Pipenv by running the following command:

   ```bash
   pip install pipenv --user
   ```

2. Install project dependencies:

   ```bash
   pipenv install
   ```

3. Run the chatbot:

   ```bash
   pipenv run chatbot
   ```

## How to Use

### Step 1: Add Your OpenAI API Key
- On the app’s sidebar, paste your **OpenAI API key**.
- The key allows you to interact with OpenAI's services.

### Step 2: Create or Select a Knowledge Base
- **Create a New Knowledge Base**:
  - Enter a name for your knowledge base in the "Create a New Vector Store" section and click the **Create Vector Store** button.
- **Select an Existing Knowledge Base**:
  - If you have previously created knowledge bases, you can select one from the dropdown list.

### Step 3: Upload a PDF File
- After creating or selecting a knowledge base, upload a PDF document by clicking the **Choose a file** button.
- The file will be indexed and added to the selected knowledge base.

### Step 4: Chat with the Assistant
- Once a knowledge base is selected, you can interact with the assistant by typing your queries in the chat input.
- The assistant will respond based on the uploaded documents.

## Project Structure

- **`app.py`**: Main entry point for the Streamlit app.
- **`loaders/indexer.py`**: Handles indexing of uploaded documents into the knowledge base.
- **`main.py`**: Contains core functions such as handling prompts and getting responses from the OpenAI API.

## Utility Functions

- **`list_folders(directory)`**: Lists all folders in the knowledge base directory.
- **`create_new_folder(directory, folder_name)`**: Creates a new folder to store uploaded files.
- **`save_uploaded_file(uploaded_file, save_dir)`**: Saves an uploaded file to the specified directory and indexes it for later use.

## Contributing

1. Fork the project.
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any issues or questions, feel free to contact @hnaseem1.

Enjoy using the Knowledge Base Assistant App!