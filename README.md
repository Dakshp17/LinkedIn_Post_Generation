# 📝 LinkedIn Post Generator - using LangGraph
[Live Demo](https://linkedinpostgeneration-n6ipacix4ndc5bru2q4bxf.streamlit.app/)

A web-based interface for the LinkedIn Post Generator app built with Streamlit. Write, review, and iterate on LinkedIn posts using AI.

## ✨ Features

- 🤖 Multi-Agent workflow powered by LangGraph
- ✍️ AI Writer Agent generates engaging LinkedIn posts
- 👨‍⚖️ AI Reviewer Agent evaluates and improves content quality
- 🌐 Real-time web search using Tavily for current trends and statistics
- 🔄 Automatic review and refinement loop
- 📄 Professional LinkedIn posts with human-like writing style
- 🎯 Built-in quality checks before approval

---

## 🏗️ Architecture

```text
                 START
                   │
                   ▼
            Writer Agent
             (Gemini 2.5)
                   │
          Need Current Data?
           │             │
          Yes            No
           │             │
           ▼             ▼
     Tavily Search   Generate Draft
           │             │
           └──────┬──────┘
                  ▼
          Reviewer Agent
          (Llama 3.3-70B)
                  │
          Post Approved?
           │             │
          Yes            No
           │             │
           ▼             ▼
          END      Feedback to Writer
                         │
                         ▼
                  Rewrite Draft
                         │
                  (Max 3 Attempts)
```

---

## 🔄 Workflow

```text
                    User Enters Topic
                            │
                            ▼
                 Initialize LangGraph State
                            │
                            ▼
                  Writer Agent (Gemini)
                            │
                            │
             Requires Current Information?
                    ┌──────────┴──────────┐
                    │                     │
                   Yes                    No
                    │                     │
                    ▼                     ▼
            Tavily Web Search        Generate Draft
                    │                     │
                    └──────────┬──────────┘
                               ▼
                  Professional LinkedIn Draft
                               │
                               ▼
              Reviewer Agent (Llama 3.3-70B)
                               │
                               ▼
                 Quality Evaluation
          • Strong Hook
          • Valuable Takeaway
          • Easy to Read
          • 150–200 Words
          • Professional Tone
          • Engaging CTA
          • No Hashtags
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
             APPROVED                    REJECTED
                 │                           │
                 ▼                           ▼
          Final LinkedIn Post       Feedback to Writer
                                            │
                                            ▼
                                   Rewrite LinkedIn Post
                                            │
                                            ▼
                                   Maximum 3 Iterations
```

---

## ⚙️ How It Works

1. The user provides a topic for the LinkedIn post.
2. The **Writer Agent (Gemini)** generates an initial draft.
3. If recent information is required, the Writer automatically invokes **Tavily Search** to retrieve current web data.
4. The generated draft is passed to the **Reviewer Agent (Llama 3.3-70B)**.
5. The reviewer evaluates the post using predefined quality criteria:
   - Strong opening hook
   - Clear takeaway
   - Readable formatting
   - 150–200 words
   - Professional and human-like tone
   - Engaging call-to-action
   - No hashtags
6. If rejected, detailed feedback is sent back to the Writer Agent.
7. The Writer rewrites the post based on the feedback.
8. The review cycle continues until:
   - The post is approved, or
   - The maximum of **3 attempts** is reached.

---

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Framework:** LangGraph
- **LLM Framework:** LangChain
- **Writer Model:** Gemini 2.5 Flash Lite
- **Reviewer Model:** Llama 3.3 70B (Groq)
- **Search Tool:** Tavily Search API
- **Environment Management:** python-dotenv

---

## 📂 Project Structure

```text
LinkedIn_Post_Generation/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
└── ...
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Dakshp17/LinkedIn_Post_Generation.git
```

Move into the project

```bash
cd LinkedIn_Post_Generation
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the Application

```bash
python app.py
```

---

## 📌 Future Improvements

- Streamlit Web Interface
- LinkedIn Carousel Generation
- AI-generated Image Suggestions
- Tone & Audience Selection
- Automatic Hashtag Generation
- LinkedIn API Integration
- Export to Markdown / PDF
- Multi-language Support

---

## 👨‍💻 Author

**Daksh Patel**

- GitHub: https://github.com/Dakshp17

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!