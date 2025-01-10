# Summarizer App  

This project is a web-based summarization app that leverages the **LaMini-Flan-T5** model to generate concise summaries for:  
1. PDF documents  
2. Online articles  
3. Custom text input
## Live Demo

Check out the live demo of this project on Hugging Face Spaces: [AI content summerizer](https://mishrasahil934-team-skulk.hf.space/?embed=true&embed_options=show_toolbar#ai-content-summarizer)


## Features  
- **PDF Summarization**: Upload a PDF file to extract and summarize its content.  
- **Article Summarization**: Enter an article URL to scrape and summarize its main content.  
- **Custom Text Summarization**: Input text manually to generate a summary.  

## Tech Stack  
- **Model**: LaMini-Flan-T5  
- **Framework**: Streamlit  
- **Libraries**:  
  - PyMuPDF: PDF text extraction  
  - BeautifulSoup: Web scraping  
  - Transformers: NLP model pipeline  

## How to Use  
1. Clone the repository:  
   ```bash
   git clone https://github.com/mishraji55/summarizer-app.git
   cd summarizer-app
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the application:  
   ```bash
   streamlit run app.py
   ```  

## Contributing  
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.  

## License  
This project is licensed under the MIT License.  

---  
Enjoy fast and accurate summarization with the power of LaMini-Flan-T5! 🚀  
