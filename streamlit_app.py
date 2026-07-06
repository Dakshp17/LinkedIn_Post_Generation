import os
import streamlit as st
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Post Container - Better contrast */
    .post-container {
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f8fb 100%);
        border-left: 5px solid #0073b1;
        border-radius: 0.75rem;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 115, 177, 0.1);
    }
    
    .post-container h3 {
        color: #0073b1;
        margin-top: 0;
        font-size: 1.3rem;
    }
    
    .post-container p {
        color: #1a1a1a;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Feedback Container - Better contrast */
    .feedback-container {
        background: linear-gradient(135deg, #fff8e6 0%, #fffdf0 100%);
        border-left: 5px solid #ff9800;
        border-radius: 0.75rem;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.1);
    }
    
    .feedback-container h4 {
        color: #f57c00;
        margin-top: 0;
        font-size: 1.2rem;
    }
    
    .feedback-container p {
        color: #2c2c2c;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Approved Container - Better contrast */
    .approved-container {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-left: 5px solid #28a745;
        border-radius: 0.75rem;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
    }
    
    .approved-container h3 {
        color: #28a745;
        margin-top: 0;
        font-size: 1.3rem;
    }
    
    .approved-container p {
        color: #1a1a1a;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #f5f5f5 !important;
        color: #1a1a1a !important;
        border: 2px solid #ddd !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
    }
    
    /* Metrics */
    .metric-box {
        background: linear-gradient(135deg, #f0f2f6 0%, #f5f7fa 100%);
        border-radius: 0.5rem;
        padding: 2rem 1.5rem;
        text-align: center;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-box h3 {
        color: #0073b1;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0073b1;
        margin-top: 0.5rem;
    }
    
    /* Attempt badge */
    .attempt-badge {
        display: inline-block;
        background-color: #0073b1;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: bold;
        font-size: 1rem;
    }
    
    /* Header styling */
    h1 {
        color: #0073b1 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #0073b1 !important;
        border-bottom: 2px solid #0073b1 !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-left: 5px solid #6c63ff;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a1a1a;
    }
    
    .info-box p {
        margin: 0;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "graph_app" not in st.session_state:
    # Setup tools and LLMs
    search_tool = TavilySearch(max_result=3)
    tools = [search_tool]

    # LLMs
    writer_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.7
    )
    writer_llm_with_tools = writer_llm.bind_tools(tools)
    reviewer_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )

    # State class
    class State(TypedDict):
        topic: str
        messages: Annotated[list, add_messages]
        draft: str
        review_feedback: str
        is_approved: bool
        attempt: int

    # System prompts
    WRITER_SYSTEM_PROMPT = (
        "You are an expert LinkedIn content writer. Your job is to write "
        "engaging, professional LinkedIn posts about the given topic. "
        "If the topic requires up-to-date information, statistics, or "
        "current trends, use the web search tool to gather fresh context "
        "before writing. If you have already received feedback on a "
        "previous draft, carefully address every point in the new draft. "
        "Rules for good LinkedIn posts: strong hook in the first line, "
        "1 clear takeaway, easy to skim (short paragraphs), around "
        "150–200 words, ends with a question or call-to-action to invite "
        "engagement. Do not use hashtags."
    )

    REVIEWER_SYSTEM_PROMPT = (
        "You are a strict LinkedIn content reviewer. You judge whether a "
        "post is publish-ready. Evaluate against these criteria:\n"
        "1. Strong hook in the first line\n"
        "2. One clear, valuable takeaway\n"
        "3. Easy to skim — uses short paragraphs\n"
        "4. Roughly 150-200 words\n"
        "5. Ends with an engaging question or CTA\n"
        "6. Professional but human tone (not corporate-robotic)\n"
        "7. No hashtags\n\n"
        "Respond in exactly this format:\n"
        "VERDICT: APPROVED or REJECTED\n"
        "FEEDBACK: <one short paragraph explaining why>\n\n"
        "Be strict but fair. Approve only if the post genuinely meets all "
        "criteria. Reject if even one criterion is clearly missing."
    )

    # Node functions
    def writer_node(state: State) -> dict:
        """Writes (or rewrites) the LinkedIn post."""
        attempt = state.get("attempt", 0) + 1
        topic = state["topic"]
        previous_feedback = state["review_feedback"]

        if attempt == 1:
            user_message = (
                f"Write a LinkedIn post on this topic: {topic}\n"
                f"If you need current info, search the web first."
            )
        else:
            user_message = (
                f"Your previous draft on '{topic}' was rejected.\n"
                f"Here is the reviewer's feedback:\n\n{previous_feedback}\n\n"
                f"Write a new, improved draft that fixes every issue mentioned. "
                f"Do not repeat the same mistake."
            )

        messages = [("system", WRITER_SYSTEM_PROMPT), ("human", user_message)]
        response = writer_llm_with_tools.invoke(messages)

        return {
            "messages": [("human", user_message), response],
            "attempt": attempt,
        }

    tool_node = ToolNode(tools)

    def extract_draft_node(state: State) -> dict:
        """Extracts the draft from the last message."""
        last_message = state["messages"][-1]
        draft = last_message.content
        return {"draft": draft}

    def reviewer_node(state: State) -> dict:
        """Reviews the draft and decides: approve or reject."""
        draft = state["draft"]
        prompt = f"Review this LinkedIn post draft:\n\n{draft}\n\nGive your review."
        response = reviewer_llm.invoke(
            [("system", REVIEWER_SYSTEM_PROMPT), ("human", prompt)]
        )
        review_text = response.content.strip()

        is_approved = "APPROVED" in review_text.upper().split("FEEDBACK")[0]

        if "FEEDBACK:" in review_text:
            feedback = review_text.split("FEEDBACK:", 1)[1].strip()
        else:
            feedback = review_text

        return {
            "review_feedback": feedback,
            "is_approved": is_approved,
        }

    # Router functions
    def should_use_tool(state: State):
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "tools"
        return "extract_draft"

    def should_stop_looping(state: State):
        if state["is_approved"]:
            return END
        if state["attempt"] >= 3:
            return END
        return "writer"

    # Build graph
    graph = StateGraph(State)
    graph.add_node("writer", writer_node)
    graph.add_node("tools", tool_node)
    graph.add_node("extract_draft", extract_draft_node)
    graph.add_node("reviewer", reviewer_node)

    graph.add_edge(START, "writer")
    graph.add_conditional_edges("writer", should_use_tool)
    graph.add_edge("tools", "reviewer")
    graph.add_edge("extract_draft", "reviewer")
    graph.add_conditional_edges("reviewer", should_stop_looping)

    app = graph.compile()
    st.session_state.graph_app = app


# UI Layout
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #0073b1; font-size: 2.5rem; margin-bottom: 0.5rem;">📝 LinkedIn Post Generator</h1>
    <p style="color: #666; font-size: 1.1rem; margin: 0;">AI-powered writing, intelligent reviewing, and automatic iteration</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### 📌 What should your post be about?")
    topic = st.text_input(
        "Enter your topic",
        placeholder="e.g., 'The future of AI in software development'",
        label_visibility="collapsed",
    )

with col2:
    st.markdown("### ⚙️ Settings")
    max_attempts = st.slider(
        "Max revisions",
        min_value=1,
        max_value=5,
        value=3,
        help="How many times should the AI revise if rejected",
        label_visibility="collapsed"
    )

st.markdown("---")

# Helpful tips
with st.expander("💡 Example Topics", expanded=False):
    st.markdown("""
Here are some good LinkedIn post topics:

- The future of AI in your industry
- Lessons learned from a recent project
- Industry trends and predictions
- Team culture and company values
- Career growth and skill development
- New technologies and tools
- Problem-solving strategies
- Data-driven insights from your field
- Leadership tips and management insights
- Work-life balance in tech
    """)

st.markdown("")

# Generate button
if st.button("🚀 Generate Post", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("❌ Please enter a topic")
    else:
        with st.spinner("🎯 Starting generation..."):
            initial_state = {
                "topic": topic,
                "messages": [],
                "draft": "",
                "review_feedback": "",
                "is_approved": False,
                "attempt": 0,
            }

            try:
                final_state = st.session_state.graph_app.invoke(initial_state)

                # Display results
                st.markdown("---")
                st.success("✅ Generation Complete!")

                # Create tabs for better organization
                tab1, tab2, tab3 = st.tabs(["📄 Final Post", "📊 Details", "💬 Review History"])

                with tab1:
                    if final_state["is_approved"]:
                        # Create HTML with proper escaping
                        post_text = final_state["draft"].replace('"', '&quot;').replace('\n', '<br>')
                        st.markdown(
                            f'<div class="approved-container">'
                            f'<h3>✅ Post Approved & Ready to Publish</h3>'
                            f'<div style="white-space: pre-wrap; color: #1a1a1a; line-height: 1.8;">{post_text}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        st.success("This post meets all LinkedIn quality standards!")
                    else:
                        post_text = final_state["draft"].replace('"', '&quot;').replace('\n', '<br>')
                        st.markdown(
                            f'<div class="post-container">'
                            f'<h3>📝 Final Draft (Needs Review)</h3>'
                            f'<div style="white-space: pre-wrap; color: #1a1a1a; line-height: 1.8;">{post_text}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        st.info("This post didn't meet all criteria. You can copy it and edit it manually.")

                    # Copy section
                    st.markdown("---")
                    st.markdown("### 📋 Copy Your Post")
                    st.text_area(
                        "Select all and copy:",
                        value=final_state["draft"],
                        height=250,
                        label_visibility="collapsed",
                        disabled=False,
                    )
                    
                    # Copy to clipboard button
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.info("✨ Click in the box above and press Ctrl+A, then Ctrl+C to copy")

                with tab2:
                    st.markdown("### 📊 Generation Statistics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(
                            f'<div class="metric-box">'
                            f'<div style="color: #666; font-size: 0.95rem; margin-bottom: 0.5rem;">📊 Attempts</div>'
                            f'<div class="metric-value">{final_state["attempt"]}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        status = "✅ APPROVED" if final_state["is_approved"] else "⏸️ PENDING"
                        status_color = "#28a745" if final_state["is_approved"] else "#ff9800"
                        st.markdown(
                            f'<div class="metric-box">'
                            f'<div style="color: #666; font-size: 0.95rem; margin-bottom: 0.5rem;">Status</div>'
                            f'<div class="metric-value" style="color: {status_color};">{status}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        word_count = len(final_state["draft"].split())
                        st.markdown(
                            f'<div class="metric-box">'
                            f'<div style="color: #666; font-size: 0.95rem; margin-bottom: 0.5rem;">📝 Words</div>'
                            f'<div class="metric-value">{word_count}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("---")
                    
                    st.markdown(
                        """
                        <div style='background: #f5f7fa; border-radius: 0.5rem; padding: 1.5rem; margin: 1rem 0;'>
                            <h3 style='color: #0073b1; margin-top: 0;'>📌 Post Details</h3>
                            
                            <div style='margin: 1rem 0;'>
                                <p style='color: #666; font-weight: bold; margin: 0.5rem 0;'>📝 Topic:</p>
                                <p style='color: #1a1a1a; font-size: 1.1rem; margin: 0.5rem 0;'>{}</p>
                            </div>
                            
                            <div style='margin: 1rem 0;'>
                                <p style='color: #666; font-weight: bold; margin: 0.5rem 0;'>✨ Quality Status:</p>
                                <p style='color: #1a1a1a; font-size: 1.1rem; margin: 0.5rem 0;'>{}</p>
                            </div>
                        </div>
                        """.format(
                            final_state['topic'],
                            "✅ Meets all LinkedIn best practices" if final_state["is_approved"] else "⚠️ Check Review History tab for feedback"
                        ),
                        unsafe_allow_html=True
                    )

                with tab3:
                    if final_state["review_feedback"]:
                        feedback_text = final_state["review_feedback"].replace('"', '&quot;').replace('\n', '<br>')
                        st.markdown(
                            f'<div class="feedback-container">'
                            f'<h4>📋 Last Review Feedback</h4>'
                            f'<div style="white-space: pre-wrap; color: #2c2c2c; line-height: 1.8; font-size: 1rem;">{feedback_text}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        
                        st.markdown("---")
                        st.markdown("### 💡 What This Means")
                        
                        if final_state["is_approved"]:
                            st.success("""
✅ **Your post was approved!** This means it:
- Has a strong hook that grabs attention
- Contains one clear, valuable takeaway
- Is easy to skim with short paragraphs
- Is around 150-200 words
- Ends with an engaging question or CTA
- Maintains a professional but human tone
- Doesn't use hashtags
                            """)
                        else:
                            st.warning("""
⚠️ **Your post needs improvements.** The feedback above explains which criteria weren't fully met.
Consider these LinkedIn best practices:
1. **Hook**: First line must be compelling
2. **Takeaway**: One clear, actionable insight
3. **Readability**: Short paragraphs, white space
4. **Length**: Aim for 150-200 words
5. **CTA**: End with a question or call-to-action
6. **Tone**: Professional yet relatable
7. **Hashtags**: Avoid them entirely
                            """)
                    else:
                        st.info("No review feedback available yet")

            except Exception as e:
                st.markdown("---")
                st.error(f"❌ An error occurred during generation", icon="❌")
                
                error_msg = str(e)
                
                if "Invalid API Key" in error_msg:
                    st.warning("""
### 🔑 API Key Issue
One of your API keys is invalid or expired:
- **GOOGLE_API_KEY** - Get from: https://aistudio.google.com/app/apikey
- **GROQ_API_KEY** - Get from: https://console.groq.com/keys  
- **TAVILY_API_KEY** - Get from: https://tavily.com

**To fix:**
1. Get fresh API keys from the links above
2. Update your `.env` file
3. Restart this app (stop and run again)
                    """)
                else:
                    st.info(f"**Error details:** {error_msg}")
                    st.info("Make sure all API keys (GOOGLE_API_KEY, GROQ_API_KEY, TAVILY_API_KEY) are properly set in your .env file")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f0f2f6 0%, #f5f7fa 100%); border-radius: 0.5rem; margin-top: 3rem;'>
        <h3 style='color: #0073b1; margin: 0.5rem 0;'>🚀 Powered By</h3>
        <p style='color: #666; margin: 0.5rem 0; font-size: 0.95rem;'>
            <strong>LangGraph</strong> • <strong>Google Gemini</strong> • <strong>Groq Llama</strong> • <strong>Tavily Search</strong>
        </p>
        <p style='color: #999; margin: 1rem 0 0 0; font-size: 0.85rem;'>
            ✨ Generate, Review & Iterate Until Perfect
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)