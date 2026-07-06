# 📝 LinkedIn Post Generator - Streamlit GUI
[Live Demo](https://linkedinpostgeneration-n6ipacix4ndc5bru2q4bxf.streamlit.app/)

A web-based interface for the LinkedIn Post Generator app built with Streamlit. Write, review, and iterate on LinkedIn posts using AI.

## 🎯 Features

- **Easy Topic Input**: Simple interface to specify your LinkedIn post topic
- **Real-time Generation**: Watch as your post is generated and reviewed
- **Multi-step Workflow**: Automatic iteration up to 3 times until post is approved
- **Clean Tabs**: Organized view for final post, details, and review history
- **Copy-Paste Ready**: Easy text area to copy your final post
- **Metrics Display**: Shows attempt count, approval status, and word count
- **Beautiful UI**: Professional styling with LinkedIn-inspired colors

## 📋 Prerequisites

You'll need API keys for:
1. **Google Generative AI (Gemini)** - For writing
2. **Groq** - For reviewing  
3. **Tavily** - For web search

Get them from:
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Groq Console](https://console.groq.com)
- [Tavily API](https://tavily.com)

## 🚀 Setup

### 1. Clone/Download Files
Make sure you have:
- `streamlit_app.py`
- `requirements.txt`
- `.env` file (create in same directory)

### 2. Create `.env` File
```bash
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Streamlit App
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 💻 Usage

1. **Enter Topic**: Type your desired LinkedIn post topic in the input field
2. **Adjust Settings** (optional): Set max attempts (1-5)
3. **Click Generate**: Press the "🚀 Generate Post" button
4. **Review Results**: 
   - **📄 Final Post**: View your approved/final post
   - **📊 Details**: See metrics like word count and approval status
   - **💬 Review History**: Check the last review feedback
5. **Copy**: Use the text area to copy your post

## 🔧 How It Works

1. **Writer Node**: Generates initial post or revises based on feedback
2. **Tool Node**: Can search the web via Tavily for current info
3. **Reviewer Node**: Evaluates post against LinkedIn best practices
4. **Router Logic**: Approves, rejects with feedback, or caps at 3 attempts

### Evaluation Criteria
Posts must have:
- ✅ Strong hook in first line
- ✅ One clear, valuable takeaway
- ✅ Easy-to-skim format (short paragraphs)
- ✅ ~150-200 words
- ✅ Engaging question or CTA at end
- ✅ Professional but human tone
- ✅ No hashtags

## 📊 Settings

- **Max Attempts**: How many times the writer can revise before giving up (1-5)
  - Default: 3
  - Set higher for more polish, lower for faster results

## ⚙️ Customization

### Change Models
Edit `streamlit_app.py`:

```python
# Writer model
writer_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",  # Change here
    temperature=0.7
)

# Reviewer model
reviewer_llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Change here
    temperature=0.2
)
```

### Adjust System Prompts
Modify `WRITER_SYSTEM_PROMPT` or `REVIEWER_SYSTEM_PROMPT` in the code to change how the AI behaves.

### Styling
The CSS is in the `st.markdown()` call with `<style>` tags. Customize colors, fonts, and spacing there.

## 🐛 Troubleshooting

### "API Key Error"
- Verify all three API keys are in your `.env` file
- Check there are no extra spaces or quotes around keys
- Restart the Streamlit app after updating `.env`

### "Module not found"
- Ensure you ran `pip install -r requirements.txt`
- Use a virtual environment: 
  ```bash
  python -m venv venv
  source venv/bin/activate  # or `venv\Scripts\activate` on Windows
  pip install -r requirements.txt
  ```

### Posts keep getting rejected
- The reviewer is strict by design
- Try higher attempt count
- Refine the topic to be more specific
- Check reviewer feedback for patterns

## 📝 Example Topics

- "The Rise of AI Agents in Enterprise Software"
- "Why Remote Work is Changing Tech Culture"
- "Building Product-Market Fit: A Founder's Guide"
- "The Future of Cloud Computing in 2025"
- "Lessons Learned from Failed Startups"

## 📚 Tech Stack

- **Frontend**: Streamlit
- **Graph Orchestration**: LangGraph
- **LLM Framework**: LangChain
- **Models**: 
  - Google Gemini (Writer)
  - Groq Llama 3.3 70B (Reviewer)
- **Search**: Tavily AI

## 📄 License

This project is provided as-is for educational purposes.

## 💡 Tips

- More specific topics → better posts
- Check reviewer feedback to understand LinkedIn best practices
- Adjust temperatures in code if posts are too creative (↑) or too boring (↓)
- Web search helps for recent topics and statistics

---

Happy post generating! 🚀