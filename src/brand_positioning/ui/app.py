import streamlit as st
import logging
import time
import json
import os
from brand_positioning.core.focused_workflow import run_focused_positioning_analysis

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise in UI

# Page config
st.set_page_config(
    page_title="Brand Positioning Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 32px !important;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 24px !important;
        font-weight: 600;
        color: #374151;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    .subsection-header {
        font-size: 20px !important;
        font-weight: 500;
        color: #4b5563;
        margin: 1.5rem 0 0.75rem 0;
    }
    .brand-summary {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }
    .brand-item {
        font-size: 16px;
        font-weight: 500;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    .content-section {
        background: #fafbfc;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    .analysis-content {
        font-size: 15px;
        line-height: 1.7;
        color: #374151;
    }
    .analysis-content h1, .analysis-content h2, .analysis-content h3 {
        color: #1f2937 !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }
    .analysis-content h1 {
        font-size: 22px !important;
    }
    .analysis-content h2 {
        font-size: 20px !important;
    }
    .analysis-content h3 {
        font-size: 18px !important;
    }
    .analysis-content p {
        margin-bottom: 1rem;
    }
    .analysis-content ul, .analysis-content ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    .analysis-content li {
        margin: 0.5rem 0;
    }
    .status-text {
        font-size: 16px;
        font-weight: 500;
        color: #059669;
    }
    .tab-content {
        padding: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'openai_key' not in st.session_state:
        st.session_state.openai_key = ""
    if 'serp_key' not in st.session_state:
        st.session_state.serp_key = ""
    if 'langfuse_public' not in st.session_state:
        st.session_state.langfuse_public = ""
    if 'langfuse_secret' not in st.session_state:
        st.session_state.langfuse_secret = ""


def run_focused_positioning_with_status(brand_info):
    """Run focused positioning analysis with status updates"""
    
    # Create status tracking
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    def update_status(message, progress=None):
        """Update status in real-time"""
        with status_placeholder:
            st.markdown(f'<div class="status-text">Status: {message}</div>', unsafe_allow_html=True)
        if progress is not None:
            progress_bar.progress(progress / 100)
    
    try:
        update_status("Starting focused positioning analysis...", 5)
        
        # Run focused analysis
        result = run_focused_positioning_analysis(brand_info, status_callback=update_status)
        
        if result.get("success"):
            update_status("Focused positioning analysis completed!", 100)
            st.success("Analysis completed! Found your niche and strategic move.")
            return result
        else:
            update_status(f"Analysis failed: {result.get('error', 'Unknown error')}", 100)
            st.error(f"Focused analysis failed: {result.get('error', 'Unknown error')}")
            return None
        
    except Exception as e:
        update_status(f"Analysis failed: {str(e)}", 100)
        st.error(f"Focused analysis failed: {str(e)}")
        return None


def display_focused_results(result):
    """Display focused positioning results in a clean, founder-friendly format"""
    
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
        return
    
    # Brand Info Summary
    st.markdown('<div class="section-header">Your Positioning Strategy</div>', unsafe_allow_html=True)
    brand_info = result.get("brand_info", {})
    
    st.markdown(f'''
    <div class="brand-summary">
        <div class="brand-item"><strong>Brand:</strong> {brand_info.get('brand', 'N/A')}</div>
        <div class="brand-item"><strong>Product:</strong> {brand_info.get('product', 'N/A')}</div>
        <div class="brand-item"><strong>Target Audience:</strong> {brand_info.get('target', 'N/A')}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Main Results - Clean, Focused Display
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="subsection-header">🎯 Your Specific Niche</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        niche_content = result.get("niche_positioning", "No positioning data available")
        st.markdown(niche_content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="subsection-header">⚡ Your Strategic Move</div>', unsafe_allow_html=True)
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        strategic_content = result.get("strategic_move", "No strategic move available")
        st.markdown(strategic_content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Cost and efficiency info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("API Calls Used", result.get("api_calls_used", "4"))
    with col2:
        st.metric("Estimated Cost", result.get("cost_estimate", "$0.20"))
    with col3:
        st.metric("Analysis Time", "1-2 minutes")


def main():
    """Main application function"""
    
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">Brand Positioning Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-powered competitive intelligence and positioning strategy for enterprise brands</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Show current mode
        from brand_positioning.config import Config
        mode_info = Config.get_mode_info()
        
        st.markdown("### Current Mode")
        if Config.DEV_MODE:
            st.warning(f"**{mode_info['mode']} Mode** - Limited SerpAPI calls for testing")
        else:
            st.success(f"**{mode_info['mode']} Mode** - Full market intelligence")
        
        st.markdown("### How it works")
        st.markdown(f"""
        **Focused Positioning Analysis:**
        1. **Find Your Niche**: Specific positioning you can dominate ({mode_info['serp_calls']} SerpAPI calls)
        2. **Strategic Move**: One smart action to gain positioning advantage
        
        **Time:** {mode_info['estimated_time']}  
        **Cost:** ~{mode_info['estimated_cost']} in AI/API calls
        
        *Perfect for founders who need clear, actionable positioning insights.*
        """)
        
        st.markdown("### Built with")
        st.markdown("- CrewAI Multi-Agent System")
        st.markdown("- GPT-4o for Strategic Analysis") 
        st.markdown("- SerpAPI for Market Research")
        st.markdown("- Langfuse for Observability")
        
        # Mode switching info
        st.markdown("### Mode Configuration")
        if Config.DEV_MODE:
            st.info("Set `DEV_MODE=false` in environment to enable production mode with full SerpAPI usage.")
        else:
            st.info("Running in production mode with comprehensive market intelligence.")
        
        # API Usage Info
        search_config = Config.get_search_config()
        st.markdown("### API Usage Details")
        st.markdown(f"- Gap research calls: {search_config['gap_research_calls']}")
        st.markdown(f"- Opportunity research calls: {search_config['opportunity_calls']}")
        st.markdown(f"- Results per search: {search_config['results_per_search']}")
        st.markdown(f"- **Total SerpAPI calls: {search_config['total_serp_calls']}** (80% reduction!)")
        
        # API Keys Status
        st.markdown("### API Keys Status")
        openai_configured = bool(os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_key"))
        serp_configured = bool(os.getenv("SERP_API_KEY") or st.session_state.get("serp_key"))
        
        if openai_configured:
            st.success("✅ OpenAI API key configured")
        else:
            st.error("❌ OpenAI API key needed")
            
        if serp_configured:
            st.success("✅ SerpAPI key configured")
        else:
            st.error("❌ SerpAPI key needed")
        
        # Observability Section
        st.markdown("### Observability")
        langfuse_configured = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
        if langfuse_configured:
            st.success("✅ Langfuse tracking enabled")
            st.markdown("📊 [View Traces](https://us.cloud.langfuse.com)")
        else:
            st.info("💡 Langfuse optional - add keys for tracking")
    
    # Main content area
    st.markdown("---")
    
    # API Configuration Section
    st.markdown('<div class="section-header">API Configuration</div>', unsafe_allow_html=True)
    
    # Check if required keys are available
    has_openai = bool(os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_key"))
    has_serp = bool(os.getenv("SERP_API_KEY") or st.session_state.get("serp_key"))
    
    with st.expander("🔑 Enter Your API Keys", expanded=not (has_openai and has_serp)):
        st.markdown("**Required for analysis:**")
        st.markdown("💡 *Keys are stored only for your session and never saved permanently*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-proj-...",
                help="Get your key from https://platform.openai.com/api-keys"
            )
            
        with col2:
            serp_key = st.text_input(
                "SerpAPI Key", 
                type="password",
                placeholder="Your SerpAPI key...",
                help="Get your key from https://serpapi.com/dashboard (free tier available)"
            )
        
        # Optional Langfuse keys
        st.markdown("**Optional (for observability):**")
        
        col3, col4 = st.columns(2)
        
        with col3:
            langfuse_public = st.text_input(
                "Langfuse Public Key",
                type="password", 
                placeholder="pk-lf-...",
                help="Optional: For tracking analysis performance"
            )
            
        with col4:
            langfuse_secret = st.text_input(
                "Langfuse Secret Key",
                type="password",
                placeholder="sk-lf-...",
                help="Optional: Pairs with public key"
            )
        
        if st.button("💾 Save API Keys", type="secondary"):
            # Update session state and environment
            if openai_key:
                st.session_state.openai_key = openai_key
                os.environ["OPENAI_API_KEY"] = openai_key
                st.success("OpenAI API key saved!")
                
            if serp_key:
                st.session_state.serp_key = serp_key  
                os.environ["SERP_API_KEY"] = serp_key
                st.success("SerpAPI key saved!")
                
            if langfuse_public:
                st.session_state.langfuse_public = langfuse_public
                os.environ["LANGFUSE_PUBLIC_KEY"] = langfuse_public
                
            if langfuse_secret:
                st.session_state.langfuse_secret = langfuse_secret
                os.environ["LANGFUSE_SECRET_KEY"] = langfuse_secret
                
            if langfuse_public and langfuse_secret:
                st.success("Langfuse keys saved!")
    
    if not (has_openai and has_serp):
        st.warning("⚠️ Please enter your OpenAI and SerpAPI keys above to run analysis")
        st.markdown("**Quick Setup:**")
        st.markdown("1. **OpenAI**: https://platform.openai.com/api-keys (~$0.15 per analysis)")  
        st.markdown("2. **SerpAPI**: https://serpapi.com/dashboard (free tier: 100 searches/month, only 4 searches per analysis)")
        st.markdown("3. Enter keys above and click 'Save API Keys'")
        st.markdown("💰 **Total cost per analysis: ~$0.20** (very affordable!)")
    
    # Input form
    with st.form("brand_input_form"):
        st.markdown("### Brand Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            brand_name = st.text_input(
                "Brand Name",
                placeholder="e.g., VitalBloom",
                help="Your brand or company name"
            )
            
            product_description = st.text_area(
                "Product Description",
                placeholder="e.g., AI-powered SaaS platform for small businesses",
                help="What does your product do? Be specific but concise.",
                height=100
            )
        
        with col2:
            target_audience = st.text_input(
                "Target Audience (Optional)",
                placeholder="e.g., Tech entrepreneurs 25-45",
                help="Who is your ideal customer? Leave blank if unsure."
            )
            
        
        # Submit button
        submitted = st.form_submit_button(
            "Run Brand Positioning Analysis",
            type="primary",
            use_container_width=True
        )
        
        # Validation and processing
        if submitted:
            # Check API keys first
            current_openai = os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_key")
            current_serp = os.getenv("SERP_API_KEY") or st.session_state.get("serp_key")
            
            if not current_openai or not current_serp:
                st.error("⚠️ Missing API keys! Please enter your OpenAI and SerpAPI keys above.")
                st.stop()
            elif not brand_name.strip():
                st.error("Please enter a brand name")
            elif not product_description.strip():
                st.error("Please enter a product description")
            else:
                # Ensure keys are set in environment for this session
                os.environ["OPENAI_API_KEY"] = current_openai
                os.environ["SERP_API_KEY"] = current_serp
                # Prepare brand info
                brand_info = {
                    "brand": brand_name.strip(),
                    "product": product_description.strip(),
                    "target": target_audience.strip() if target_audience.strip() else "general market"
                }
                
                # Run focused positioning analysis
                st.markdown('<div class=\"section-header\">Analysis in Progress</div>', unsafe_allow_html=True)
                st.markdown("**Expected Time:** 1-2 minutes with focused research")
                st.markdown("**API Usage:** Only 4 SerpAPI calls ($0.20 cost)")
                
                result = run_focused_positioning_with_status(brand_info)
                
                if result and result.get("success"):
                    st.markdown("---")
                    display_focused_results(result)
                else:
                    st.error(f"Analysis failed: {result.get('error', 'Unknown error') if result else 'Unknown error'}")
    

if __name__ == "__main__":
    main()