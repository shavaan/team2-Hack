# Multi-PDF Law Analysis System

A comprehensive system for analyzing multiple legal documents against various topics using Azure Document Intelligence and OpenAI services. The system extracts relevant law sections, performs semantic analysis, and generates detailed reports.

## 🚀 Quick Start

```bash
# Interactive setup guide
python main.py demo --quick-start

# Run focused analysis with sample document
python main.py demo --focused

# Run full analysis
python main.py demo
```

## 📁 Project Structure

```
hackathon/
├── src/                                    # Source code
│   ├── services/                          # Core services
│   │   ├── document_intelligence/         # PDF text extraction
│   │   ├── rag_chatbot/                   # Semantic analysis & RAG
│   │   ├── law_analysis_service.py       # Main orchestrator
│   │   └── report_generator.py           # Multi-format reporting
│   ├── utils/                             # Utilities
│   │   └── pdf_manager.py                # PDF management
│   └── shared/                            # Shared authentication
├── demos/                                 # Demo scripts
│   ├── multi_pdf_demo.py                 # Main demo
│   ├── quick_start.py                    # Interactive setup
│   └── ...
├── tests/                                 # Test scripts
├── docs/                                  # Documentation
├── pdfs/                                  # PDF documents
├── reports/                               # Generated reports
├── archive/                               # Old/backup files
├── main.py                               # Main entry point
└── README.md                             # This file
```

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. Required Python packages:
   ```bash
   pip install requests python-dotenv numpy
   ```

### Configuration

#### Document Intelligence Service

1. Navigate to the `document_intelligence/` directory
2. Copy `.env.example` to `.env`
3. Fill in your Azure credentials and endpoints in the `.env` file:
   ```
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   AZURE_SCOPE=https://cognitiveservices.azure.com/.default
   DOCUMENT_INTELLIGENCE_ENDPOINT=your_document_intelligence_endpoint
   DOCUMENT_INTELLIGENCE_SUBSCRIPTION_KEY=your_subscription_key
   PDF_FILE_PATH=path_to_your_pdf_file
   ```

#### RAG Chatbot Service

1. Navigate to the `rag_chatbot/` directory
2. Copy `.env.example` to `.env`
3. Fill in your Azure credentials and OpenAI endpoints in the `.env` file:
   ```
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   AZURE_SCOPE=https://cognitiveservices.azure.com/.default
   AZURE_OPENAI_CHAT_ENDPOINT=your_chat_endpoint
   AZURE_OPENAI_EMBEDDINGS_ENDPOINT=your_embeddings_endpoint
   AZURE_OPENAI_SUBSCRIPTION_KEY=your_openai_subscription_key
   ```

## Usage

### Document Intelligence Service

```python
from document_intelligence.service import DocumentIntelligenceService

# Initialize service
service = DocumentIntelligenceService()

# Analyze a document
results = service.analyze_document("path/to/your/document.pdf")

if 'error' not in results:
    print(f"Total pages: {results['total_pages']}")
    print(f"Has handwritten content: {results['has_handwritten_content']}")
else:
    print(f"Error: {results['error']}")
```

### RAG Chatbot Service

```python
from rag_chatbot.service import RAGChatbotService

# Initialize service
service = RAGChatbotService()

# Create knowledge base
documents = [
    "Your document content here...",
    "More document content...",
]
knowledge_base = service.create_knowledge_base(documents)

# Perform RAG query
response = service.rag_query("Your question here", knowledge_base)
print(response)
```

### Running the Demo Scripts

#### Document Intelligence Demo
```bash
cd document_intelligence
python service.py
```

#### RAG Chatbot Demo
```bash
cd rag_chatbot
python service.py
```

## Features

### Shared Authentication Module
- OAuth2 client credentials flow
- Token management
- Environment variable validation

### Document Intelligence Service
- PDF document analysis
- Text extraction
- Handwriting detection
- Page-by-page processing
- Structured result formatting

### RAG Chatbot Service
- Document embedding generation
- Vector similarity search
- Context-aware chat responses
- Knowledge base creation
- Retrieval-augmented generation

## Security Notes

- Never commit `.env` files to version control
- Use environment variables for all sensitive configuration
- Rotate credentials regularly
- Use Azure Key Vault for production deployments

## API Endpoints Used

### Document Intelligence
- Endpoint: Azure Document Intelligence API v2024-11-30
- Model: prebuilt-layout

### Azure OpenAI
- Chat Completions: gpt-35-turbo model
- Embeddings: text-embedding-3-large model

## Error Handling

Both services include comprehensive error handling for:
- Authentication failures
- API rate limits
- Network connectivity issues
- Invalid responses
- Missing configuration

## Troubleshooting

1. **Authentication Issues**: Verify your Azure AD credentials and permissions
2. **API Errors**: Check endpoint URLs and subscription keys
3. **File Not Found**: Ensure PDF file paths are correct and accessible
4. **Module Import Errors**: Verify Python path and package installations

## Archive Directory

The `archive/` directory contains the original non-modularized files from before the project refactoring:

- `documentIntelligence.py` - Original monolithic Document Intelligence script
- `azure_openai_rag.py` - Original combined RAG chatbot implementation  
- `test_azure_openai.py` - Basic API test scripts
- `enhanced_rag_demo.py` - Enhanced RAG demonstration

These files are kept for historical reference and show the evolution from a monolithic to modular architecture. See `archive/README.md` for more details.
