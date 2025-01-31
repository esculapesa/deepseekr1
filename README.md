# Local ChatPDF with DeepSeek R1

**ChatPDF** is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and interact with them through a chatbot interface. The system uses advanced embedding models and a local vector store for efficient and accurate question-answering.

## Features

- **PDF Upload**: Upload one or multiple PDF documents to enable question-answering across their combined content.
- **RAG Workflow**: Combines retrieval and generation for high-quality responses.
- **Profile Management**: Create and manage profiles to organize your PDFs (Replit-only feature).
- **Customizable Retrieval**: Adjust the number of retrieved results (`k`) and similarity threshold to fine-tune performance.
- **Memory Management**: Easily clear vector store and retrievers to reset the system.
- **Streamlit Interface**: A user-friendly web application for seamless interaction.

## Installation

### Running on Replit (Recommended)

1. Fork the repository on Replit
2. Click the Run button
3. The application will automatically set up and start

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/esculapesa/deepseekr1.git
cd deepseekr1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama from https://ollama.ai

4. Pull required models:
```bash
ollama pull mxbai-embed-large
ollama pull deepseek-r1:latest
```

5. Start Ollama service:
```bash
ollama serve
```

6. Create a simple `profile_manager.py` to work locally:
```python
class ProfileManager:
    def __init__(self):
        self.profiles = {}
        self.current_profile = None

    def create_profile(self, name: str):
        if name not in self.profiles:
            self.profiles[name] = {"pdfs": []}
            self.current_profile = name

    def delete_profile(self, name: str):
        if name in self.profiles:
            del self.profiles[name]
            if self.current_profile == name:
                self.current_profile = None

    def add_pdf_to_profile(self, profile: str, pdf_path: str, pdf_name: str):
        if profile in self.profiles:
            if pdf_name not in self.profiles[profile]["pdfs"]:
                self.profiles[profile]["pdfs"].append(pdf_name)

    def get_profile_pdfs(self, profile: str):
        return self.profiles.get(profile, {}).get("pdfs", [])

    def load_pdf_from_profile(self, profile: str, pdf_name: str):
        if profile in self.profiles and pdf_name in self.profiles[profile]["pdfs"]:
            return None

    def get_all_profiles(self):
        return list(self.profiles.keys())
```

7. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Select or create a profile (required)
2. Upload PDF documents
3. Ask questions about the content
4. Adjust retrieval settings as needed

## Project Structure

```
.
├── app.py              # Streamlit interface
├── rag.py             # Core RAG implementation
├── profile_manager.py # Profile management
└── requirements.txt   # Dependencies
```

## Requirements

- Python 3.8+
- Ollama
- Streamlit
- LangChain
- PyPDF
- ChromaDB

## Troubleshooting

1. **NoneType Error**: Make sure you've created a profile before uploading PDFs
2. **Ollama Connection**: Ensure Ollama is running (`ollama serve`)
3. **Missing Models**: Run the ollama pull commands


## Future Enhancements

- **Memory Integration**: Add persistent memory to maintain conversational context across sessions.
- **Advanced Analytics**: Include visual insights from retrieved content.
- **Expanded Model Support**: Support additional embedding and LLM providers.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [LangChain](https://github.com/hwchase17/langchain)
- [Streamlit](https://github.com/streamlit/streamlit)
- [Ollama](https://ollama.ai/)