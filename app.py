import streamlit as st
import pandas as pd
from datetime import datetime
from config import Config
from agents.pinterest_agent import PinterestAgent
from agents.content_agent import ContentAgent
from agents.link_agent import LinkAgent
from agents.analytics_agent import AnalyticsAgent
from utils import Utils

# Page config
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        color: #E60023;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .version {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    .pin-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    .stat-card {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .success-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pinterest_agent' not in st.session_state:
    st.session_state.pinterest_agent = PinterestAgent()
    st.session_state.content_agent = ContentAgent()
    st.session_state.link_agent = LinkAgent()
    st.session_state.analytics_agent = AnalyticsAgent()
    st.session_state.generated_pins = []
    st.session_state.total_created = 0

# Header
st.markdown(f'<div class="main-title">📌 {Config.APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="version">v{Config.VERSION} - Professional Edition</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎨 Pin Generator")
    
    # Tab selection
    tab = st.radio(
        "Choose Mode:",
        ["🚀 Quick Generate", "🤖 AI Enhanced", "📊 Analytics"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if tab == "🚀 Quick Generate":
        st.subheader("Quick Settings")
        
        niche = st.selectbox(
            "Select Niche:",
            Config.get_all_niches(),
            format_func=lambda x: Config.NICHES[x]["name"]
        )
        
        template = st.selectbox(
            "Pin Style:",
            ["viral", "professional", "urgency"]
        )
        
        count = st.slider("Number of Pins:", 1, 10, 3)
        
        auto_links = st.checkbox("🔗 Auto-generate links", value=True)
        
        if st.button("✨ GENERATE PINS", type="primary", use_container_width=True):
            with st.spinner("Creating pins..."):
                # Generate pins
                new_pins = st.session_state.pinterest_agent.generate_batch(
                    niche=niche,
                    count=count,
                    template=template
                )
                
                # Add links if enabled
                if auto_links:
                    for pin in new_pins:
                        st.session_state.link_agent.add_link_to_pin(pin)
                
                # Track analytics
                for pin in new_pins:
                    st.session_state.analytics_agent.track_pin(pin)
                
                st.session_state.generated_pins = new_pins
                st.session_state.total_created += len(new_pins)
            
            st.success(f"✅ Created {len(new_pins)} pins!")
            st.balloons()
    
    elif tab == "🤖 AI Enhanced":
        st.subheader("AI-Powered Generation")
        
        niche = st.selectbox(
            "Niche:",
            Config.get_all_niches(),
            format_func=lambda x: Config.NICHES[x]["name"],
            key="ai_niche"
        )
        
        product = st.text_input(
            "Custom Product Name:",
            placeholder="e.g., Ultra HD Webcam"
        )
        
        style = st.select_slider(
            "Content Style:",
            options=["professional", "viral", "urgency"]
        )
        
        if st.button("🤖 GENERATE WITH AI", type="primary", use_container_width=True):
            with st.spinner("AI is working..."):
                if product:
                    # AI content generation
                    ai_content = st.session_state.content_agent.generate_advanced_content(
                        product, niche, style
                    )
                    
                    # Create pin with AI content
                    pin = {
                        "product": product,
                        "niche": niche,
                        "title": ai_content["title"],
                        "description": ai_content["description"],
                        "keywords": ai_content["hashtags"],
                        "created_at": datetime.now().isoformat(),
                        "ai_generated": True
                    }
                    
                    # Add link
                    st.session_state.link_agent.add_link_to_pin(pin)
                    
                    # Track
                    st.session_state.analytics_agent.track_pin(pin)
                    
                    st.session_state.generated_pins = [pin]
                    st.session_state.total_created += 1
                    
                    st.success("✅ AI pin created!")
                else:
                    st.warning("⚠️ Enter product name")
    
    else:  # Analytics tab
        st.subheader("📊 Statistics")
        
        report = st.session_state.analytics_agent.get_performance_report()
        
        st.metric("Total Pins", report.get("total_pins", 0))
        
        if report.get("by_niche"):
            st.write("**By Niche:**")
            for niche, count in report["by_niche"].items():
                st.write(f"• {niche}: {count}")
        
        if st.button("📥 Download Report"):
            st.download_button(
                "Download JSON",
                data=str(report),
                file_name=f"report_{Utils.format_timestamp()}.json"
            )
    
    st.divider()
    
    # Quick stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Ready", len(st.session_state.generated_pins))
    with col2:
        st.metric("Total", st.session_state.total_created)
# Main content area
if st.session_state.generated_pins:
    
    st.header("📋 Generated Pins")
    
    # Bulk actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Save All"):
            filename = f"pins_{Utils.format_timestamp()}.json"
            if Utils.save_to_json(st.session_state.generated_pins, filename):
                st.success(f"✅ Saved: {filename}")
    
    with col2:
        if st.button("🔗 Add Links to All"):
            for pin in st.session_state.generated_pins:
                if not pin.get("affiliate_link"):
                    st.session_state.link_agent.add_link_to_pin(pin)
            st.success("✅ Links added!")
            st.rerun()
    
    with col3:
        if st.button("🤖 Enhance All with AI"):
            for pin in st.session_state.generated_pins:
                st.session_state.content_agent.enhance_existing_content(pin)
            st.success("✅ Enhanced!")
            st.rerun()
    
    with col4:
        if st.button("🗑️ Clear All"):
            st.session_state.generated_pins = []
            st.rerun()
    
    st.divider()
    
    # Display pins
    for idx, pin in enumerate(st.session_state.generated_pins):
        
        with st.expander(
            f"📌 Pin #{idx+1}: {pin['title'][:60]}...",
            expanded=(idx == 0)
        ):
            
            # Header info
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**🏷️ Product:** {pin['product']}")
                st.markdown(f"**📂 Niche:** {pin['niche']}")
            
            with col2:
                if pin.get("ai_generated"):
                    st.success("🤖 AI Enhanced")
                if pin.get("link_platform"):
                    st.info(f"🔗 {pin['link_platform']}")
            
            with col3:
                status_color = "🟢" if pin.get("status") == "ready" else "🟡"
                st.markdown(f"{status_color} **{pin.get('status', 'draft').upper()}**")
            
            st.divider()
            
            # Content sections
            tabs = st.tabs(["📝 Content", "🔗 Link", "📋 Complete Pin"])
            
            with tabs[0]:
                # Title
                st.markdown("### Title")
                title_edited = st.text_area(
                    "Title",
                    value=pin['title'],
                    height=60,
                    key=f"title_{idx}",
                    label_visibility="collapsed"
                )
                pin['title'] = title_edited
                
                # Description
                st.markdown("### Description")
                desc_edited = st.text_area(
                    "Description",
                    value=pin['description'],
                    height=120,
                    key=f"desc_{idx}",
                    label_visibility="collapsed"
                )
                pin['description'] = desc_edited
                
                # Keywords
                st.markdown("### Keywords")
                keywords_edited = st.text_area(
                    "Keywords",
                    value=pin.get('keywords', ''),
                    height=80,
                    key=f"keywords_{idx}",
                    label_visibility="collapsed"
                )
                pin['keywords'] = keywords_edited
            
            with tabs[1]:
                # Link management
                if pin.get('affiliate_link'):
                    st.success("✅ Link Generated")
                    st.code(pin['affiliate_link'])
                    
                    if pin.get('commission_rate'):
                        st.info(f"💰 Commission: {pin['commission_rate']}")
                    
                    # Option to change platform
                    new_platform = st.selectbox(
                        "Change platform:",
                        ["auto", "amazon", "aliexpress", "clickbank"],
                        key=f"platform_{idx}"
                    )
                    
                    if st.button("🔄 Regenerate Link", key=f"regen_{idx}"):
                        st.session_state.link_agent.add_link_to_pin(pin, new_platform)
                        st.success("✅ Link updated!")
                        st.rerun()
                
                else:
                    st.warning("⚠️ No link generated")
                    
                    if st.button("🔗 Generate Link Now", key=f"gen_{idx}"):
                        st.session_state.link_agent.add_link_to_pin(pin)
                        st.success("✅ Link added!")
                        st.rerun()
                
                # Manual link option
                st.divider()
                st.markdown("**Or paste custom link:**")
                custom_link = st.text_input(
                    "Custom link",
                    placeholder="https://...",
                    key=f"custom_{idx}",
                    label_visibility="collapsed"
                )
                
                if custom_link:
                    pin['affiliate_link'] = custom_link
                    pin['link_platform'] = "Custom"
                    st.success("✅ Custom link added!")
            
            with tabs[2]:
                # Complete pin for copying
                if pin.get('affiliate_link'):
                    st.markdown("### 📋 Ready to Post on Pinterest")
                    
                    complete_text = f"""{pin['title']}

{pin['description']}

{pin.get('cta', '👉 Click link for more info!')}

🔗 {pin['affiliate_link']}

{pin.get('keywords', '')}

#Pinterest #Trending #Shopping"""
                    
                    st.code(complete_text, language=None)
                    
                    st.markdown("""
                    **📌 How to Post:**
                    1. Copy text above
                    2. Open Pinterest app/website
                    3. Click '+' → Create Pin
                    4. Upload image (use Canva)
                    5. Paste title in title field
                    6. Paste description in description
                    7. Add destination link
                    8. Publish!
                    """)
                    
                else:
                    st.warning("⚠️ Add affiliate link first (see 'Link' tab)")

else:
    # Welcome screen
    st.info("👈 Use sidebar to generate your first pins!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🚀 Quick Generate
        - Choose niche
        - Set pin count
        - Auto-generate links
        - Instant results
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI Enhanced
        - Custom products
        - AI-powered content
        - Viral optimization
        - Higher conversions
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Analytics
        - Track performance
        - Niche insights
        - Export reports
        - Optimize strategy
        """)
    
    st.divider()
    
    st.markdown("""
    ## 🎯 Features:
    
    ✅ **Multi-Agent System** - Pinterest, Content, Link & Analytics agents working together
    
    ✅ **Auto Link Generation** - Amazon, AliExpress, ClickBank support
    
    ✅ **AI-Powered Content** - GPT-4 integration for viral pins
    
    ✅ **Multiple Templates** - Viral, Professional, Urgency styles
    
    ✅ **Bulk Operations** - Generate, enhance, save multiple pins
    
    ✅ **Analytics Dashboard** - Track performance and optimize
    
    ✅ **Fully Customizable** - Edit any content before posting
    
    ✅ **Export Ready** - Download pins in JSON format
    """)

# Footer
st.divider()
st.caption(f"💡 {Config.APP_NAME} v{Config.VERSION} | Built with Streamlit | Powered by AI")
