import streamlit as st
import logging
import time
import json
from brand_positioning.core.parallel_crews import run_parallel_analysis_sync, run_parallel_intelligence_sync

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
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

def run_full_analysis_with_status(brand_info):
    """Run the complete brand positioning analysis with parallel crews"""
    
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
        update_status("Initializing parallel crews...", 5)
        
        # Run parallel analysis
        result = run_parallel_analysis_sync(brand_info, status_callback=update_status)
        
        if result.get("success"):
            update_status("Analysis completed successfully!", 100)
            st.success("Parallel analysis completed!")
            return result
        else:
            update_status(f"Analysis failed: {result.get('error', 'Unknown error')}", 100)
            st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
            return None
        
    except Exception as e:
        update_status(f"Analysis failed: {str(e)}", 100)
        st.error(f"Analysis failed: {str(e)}")
        return None

def run_quick_analysis_with_status(brand_info):
    """Run quick parallel market intelligence only"""
    
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
        update_status("Starting parallel market intelligence...", 5)
        
        # Run parallel intelligence only
        result = run_parallel_intelligence_sync(brand_info, status_callback=update_status)
        
        if result.get("success"):
            update_status("Market intelligence completed!", 100)
            st.success("Parallel market intelligence completed!")
            return result
        else:
            update_status(f"Analysis failed: {result.get('error', 'Unknown error')}", 100)
            st.error(f"Quick analysis failed: {result.get('error', 'Unknown error')}")
            return None
        
    except Exception as e:
        update_status(f"Analysis failed: {str(e)}", 100)
        st.error(f"Quick analysis failed: {str(e)}")
        return None

def display_results(result):
    """Display the analysis results in a structured format"""
    
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
        return
    
    # Brand Info Summary
    st.markdown('<div class="section-header">Analysis Summary</div>', unsafe_allow_html=True)
    brand_info = result.get("brand_info", {})
    
    st.markdown(f'''
    <div class="brand-summary">
        <div class="brand-item"><strong>Brand:</strong> {brand_info.get('brand', 'N/A')}</div>
        <div class="brand-item"><strong>Product:</strong> {brand_info.get('product', 'N/A')}</div>
        <div class="brand-item"><strong>Target Audience:</strong> {brand_info.get('target', 'N/A')}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Check if this is full analysis or quick analysis
    is_full_analysis = "positioning_strategy" in result and "strategic_actions" in result
    
    if is_full_analysis:
        # Display full results in tabs
        tab1, tab2, tab3 = st.tabs(["Market Intelligence", "Positioning Strategy", "Strategic Actions"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            intelligence = result.get("market_intelligence", {})
            if isinstance(intelligence, dict):
                st.markdown('<div class="subsection-header">Competitor Analysis</div>', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                competitor_content = intelligence.get("competitor_analysis", "No data available")
                st.markdown(competitor_content)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="subsection-header">Customer Insights</div>', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                customer_content = intelligence.get("customer_insights", "No data available")
                st.markdown(customer_content)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="subsection-header">Market Trends</div>', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                trends_content = intelligence.get("market_trends", "No data available")
                st.markdown(trends_content)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                st.markdown(str(intelligence))
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            positioning = result.get("positioning_strategy", "No data available")
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            st.markdown(positioning)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            actions = result.get("strategic_actions", "No data available")
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            st.markdown(actions)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Quick analysis - just show intelligence
        st.markdown('<div class="section-header">Market Intelligence Results</div>', unsafe_allow_html=True)
        intelligence = result.get("intelligence", {})
        if isinstance(intelligence, dict):
            tab1, tab2, tab3 = st.tabs(["Competitor Analysis", "Customer Insights", "Market Trends"])
            
            with tab1:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                st.markdown(intelligence.get("competitor_analysis", "No data available"))
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                st.markdown(intelligence.get("customer_insights", "No data available"))
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab3:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.markdown('<div class="content-section">', unsafe_allow_html=True)
                st.markdown(intelligence.get("market_trends", "No data available"))
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="content-section">', unsafe_allow_html=True)
            st.markdown(str(intelligence))
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Raw result for debugging (expandable)
    with st.expander("Full Analysis Result (Technical)"):
        st.json(result)

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
        1. **Market Intelligence**: Analyze competitors and customer insights ({mode_info['serp_calls']} SerpAPI calls)
        2. **Positioning Strategy**: Generate specific niche recommendations  
        3. **Strategic Actions**: Create prioritized action plans
        
        **Time:** {mode_info['estimated_time']}  
        **Cost:** ~{mode_info['estimated_cost']} in AI/API calls
        """)
        
        st.markdown("### Built with")
        st.markdown("- CrewAI Multi-Agent System")
        st.markdown("- GPT-4o for Strategic Analysis") 
        st.markdown("- SerpAPI for Market Research")
        
        # Mode switching info
        st.markdown("### Mode Configuration")
        if Config.DEV_MODE:
            st.info("Set `DEV_MODE=false` in environment to enable production mode with full SerpAPI usage.")
        else:
            st.info("Running in production mode with comprehensive market intelligence.")
        
        # API Usage Info
        search_config = Config.get_search_config()
        st.markdown("### API Usage Details")
        st.markdown(f"- Competitor searches: {search_config['competitor_searches']}")
        st.markdown(f"- Customer searches: {search_config['customer_searches']}")
        st.markdown(f"- Trend searches: {search_config['trend_searches']}")
        st.markdown(f"- **Total SerpAPI calls: {search_config['total_serp_calls']}**")
    
    # Main content area
    st.markdown("---")
    
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
            
            # Analysis type selector
            analysis_type = st.selectbox(
                "Analysis Type",
                [
                    "Full Analysis (Market Intelligence + Positioning + Actions)",
                    "Quick Market Intelligence Only"
                ],
                help="Full analysis takes 8-12 minutes, Quick analysis takes 3-5 minutes"
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "Run Brand Positioning Analysis",
            type="primary",
            use_container_width=True
        )
        
        # Validation and processing
        if submitted:
            if not brand_name.strip():
                st.error("Please enter a brand name")
            elif not product_description.strip():
                st.error("Please enter a product description")
            else:
                # Prepare brand info
                brand_info = {
                    "brand": brand_name.strip(),
                    "product": product_description.strip(),
                    "target": target_audience.strip() if target_audience.strip() else "general market"
                }
                
                # Run analysis based on type
                st.markdown('<div class=\"section-header\">Analysis in Progress</div>', unsafe_allow_html=True)
                
                if analysis_type == "Quick Market Intelligence Only":
                    # Quick parallel analysis
                    st.markdown("**Expected Time:** 2-4 minutes with 3 parallel crews")
                    
                    result = run_quick_analysis_with_status(brand_info)
                    
                    if result and result.get("success"):
                        st.markdown("---")
                        display_results(result)
                    else:
                        st.error(f"Quick analysis failed: {result.get('error', 'Unknown error') if result else 'Unknown error'}")
                
                else:
                    # Full parallel analysis  
                    st.markdown("**Expected Time:** 6-10 minutes with parallel crews")
                    
                    result = run_full_analysis_with_status(brand_info)
                    
                    if result and result.get("success"):
                        st.session_state.analysis_result = result
                        st.session_state.analysis_complete = True
                        st.rerun()
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_result:
        st.markdown('<div class="section-header">Analysis Results</div>', unsafe_allow_html=True)
        display_results(st.session_state.analysis_result)
        
        # Reset button
        if st.button("Run New Analysis", type="secondary"):
            st.session_state.analysis_complete = False
            st.session_state.analysis_result = None
            st.rerun()

if __name__ == "__main__":
    main()