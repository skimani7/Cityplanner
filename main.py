print("Hello There!")
import streamlit as st
import plotly.express as px
from PIL import Image
import io
import base64

#setup
st.set_page_config(
    page_title="Nairobi Budget Adventure",
    page_icon="🌆",
    layout="centered",
    initial_sidebar_state="expanded"
)

# palette
COLORS = {
    "background": "#F0F2F6",
    "text": "#2E86AB",
    "accent": "#F18F01",
    "savings": "#48A14D"
}

# Custom
st.markdown(f"""
<style>
    .stButton>button {{
        background-color: {COLORS['accent']};
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
    }}
    .stSlider>div>div>div>div {{
        background: {COLORS['accent']} !important;
    }}
    .reportview-container {{
        background: {COLORS['background']};
    }}
    h1 {{
        color: {COLORS['text']};
    }}
</style>
""", unsafe_allow_html=True)

# Nairobi neighborhoods 
NEIGHBORHOODS = {
    '🏙 Kilimani': {'rent': 65000, 'vibe': 'Trendy urban lifestyle'},
    '🌃 Westlands': {'rent': 75000, 'vibe': 'Upscale nightlife hub'},
    '🌳 Kileleshwa': {'rent': 60000, 'vibe': 'Quiet leafy streets'},
    '🏘 South B': {'rent': 45000, 'vibe': 'Affordable and central'}
}

# Transport options 
TRANSPORT = {
    '🚌 Matatus': {'cost': 8000, 'desc': "Colorful & adventurous!"},
    '🚖 Uber/Bolt': {'cost': 20000, 'desc': "Comfy but pricey rides"},
    '🚗 Personal Car': {'cost': 15000, 'desc': "Freedom + fuel costs"},
    '🏍 Boda Bodas': {'cost': 10000, 'desc': "Fast but hold tight!"}
}

# Lifestyle choices 
LIFESTYLE = {
    '🍽 Eating Out': {'cost': 15000},
    '🛒 Groceries': {'cost': 12000},
    '🎬 Entertainment': {'cost': 8000},
    '💅 Self-Care': {'cost': 5000},
    '🏋 Gym': {'cost': 4000}
}

# App header 
st.title("🌇 Nairobi Budget Adventure")
st.markdown("""
Plan your dream Nairobi lifestyle while saving for tomorrow!  
""")

# Sidebar
with st.sidebar:
    st.subheader("💰 Budget Tips")
    st.markdown("""
    - Matatus save you money but add adventure!
    - South B = 3x more savings than Westlands  
    - Cooking at home 🧑‍🍳 = More shillings for safari!  
    """)
    
    # progress tracker
    st.subheader("Your Nairobi Journey")
    budget_level = st.radio(
        "Where are you?", 
        ("🌱 Seedling", "🌿 Sprouting", "🌳 Mighty Baobab"),
        index=1
    )

# Income section feedback
with st.expander("💵 STEP 1: Your Monthly Income", expanded=True):
    income = st.slider(
        "Slide to your income (KSh)", 
        20000, 500000, 120000,
        help="Drag to match your monthly take-home pay"
    )
    st.metric("", f"KSh {income:,}")

# Neighborhood selection
with st.expander("🏠 STEP 2: Pick Your Neighborhood"):
    area = st.selectbox(
        "Where's your dream spot?", 
        list(NEIGHBORHOODS.keys()),
        format_func=lambda x: f"{x} (KSh {NEIGHBORHOODS[x]['rent']:,}) - {NEIGHBORHOODS[x]['vibe']}"
    )
    rent = NEIGHBORHOODS[area]['rent']
    st.caption(NEIGHBORHOODS[area]['vibe'])

# Transport selection
with st.expander("🚕 STEP 3: How You'll Get Around"):
    transport = st.multiselect(
        "Choose your rides:", 
        list(TRANSPORT.keys()),
        default=['🚌 Matatus'],
        format_func=lambda x: f"{x} (KSh {TRANSPORT[x]['cost']:,}) - {TRANSPORT[x]['desc']}"
    )
    transport_cost = sum(TRANSPORT[t]['cost'] for t in transport)

# Lifestyle selection
with st.expander("🎉 STEP 4: Lifestyle Choices"):
    lifestyle = st.multiselect(
        "What makes you happy?", 
        list(LIFESTYLE.keys()),
        default=['🛒 Groceries', '🎬 Entertainment'],
        format_func=lambda x: f"{x} (KSh {LIFESTYLE[x]['cost']:,})"
    )
    lifestyle_cost = sum(LIFESTYLE[l]['cost'] for l in lifestyle)

# Savings goal with 
with st.expander("💰 STEP 5: Savings Goal"):
    savings_pct = st.slider(
        "What % will you save?", 
        0, 50, 15,
        help="Even 10% adds up over time!"
    )
    savings_amount = (income * savings_pct) / 100

# Calculate button 
if st.button("✨ Calculate My Nairobi Budget"):
    total_expenses = rent + transport_cost + lifestyle_cost
    remaining = income - total_expenses - savings_amount
    
    # Show results with emoji indicators
    st.balloons()
    st.success(f"""
    ## 📊 Your Nairobi Budget Breakdown
    
    | Category        | Amount         |
    |----------------|---------------:|
    | *Income*      | KSh {income:,} |
    | *Housing*     | KSh {rent:,}   |
    | *Transport*   | KSh {transport_cost:,} |
    | *Lifestyle*   | KSh {lifestyle_cost:,} |
    | *Savings* ({savings_pct}%) | KSh {savings_amount:,} |
    | *Remaining*   | KSh {remaining:,} |
    """)
    
    #  budget tree 
    fig = px.treemap(
        names=['Income', 'Housing', 'Transport', 'Lifestyle', 'Savings', 'Remaining'],
        parents=['', 'Income', 'Income', 'Income', 'Income', 'Income'],
        values=[income, rent, transport_cost, lifestyle_cost, savings_amount, max(remaining, 0)],
        color=['Income', 'Housing', 'Transport', 'Lifestyle', 'Savings', 'Remaining'],
        color_discrete_map={
            'Income': COLORS['text'],
            'Housing': 'red',
            'Transport': 'blue',
            'Lifestyle': 'orange',
            'Savings': COLORS['savings'],
            'Remaining': 'purle'
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    #  personalized message
    if remaining < 0:
        st.error("🚨 Whoops! Your expenses exceed income. Try Westlands instead?")
    elif remaining < 10000:
        st.warning("🟡 Tight budget! Maybe fewer Uber rides this month?")
    else:
        st.success(f"""
        🎉 *You're rocking it!*  
        With KSh {remaining:,} left, you could:  
        - Treat yourself at {area.split()[-1]}'s best cafe ☕  
        - Add to your savings 💰  
        - Plan a weekend getaway 🦁  
        """)

# Footer with Sarah
st.markdown("---")
st.caption("Did you know? Nairobi means 'cool water' in Maasai. Budget wisely and enjoy Kenya's vibrant capital!")