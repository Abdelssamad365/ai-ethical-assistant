# Ethical AI Assistant

A simple web application where users can ask ethical or privacy-related questions about technology, and receive helpful, informative responses from an AI assistant.

## Features

- Clean, modern UI with responsive design
- Simple question-answer interface
- Example questions to get started
- Mobile-friendly layout

## Prerequisites

- Python 3.7+
- Flask
- An API key for an LLM provider (e.g., OpenAI)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ethical-ai-assistant.git
   cd ethical-ai-assistant
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on the example:
   ```
   cp .env.example .env
   ```

6. Edit the `.env` file and add your LLM API key.

## Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Type your ethical or privacy-related question in the input field
2. Click the send button or press Enter
3. Wait for the AI assistant to provide a response
4. Continue the conversation as needed

## Customization

- Edit `static/css/styles.css` to change the look and feel
- Modify the prompt in `app.py` to change how the AI responds to questions
- Add more example questions in `templates/index.html`

## License

This project is licensed under the [MIT License](./LICENSE).

## Disclaimer

This application is for educational purposes only. The AI responses should not be considered definitive ethical advice.
