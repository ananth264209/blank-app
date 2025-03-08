import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ✅ Set Page Config First
st.set_page_config(page_title="GearSpot - Rent & Lend Gadgets", layout="wide")

# ✅ Logo Link
LOGO_URL = "https://i.imghippo.com/files/qRZ4936Brs.png"

# ✅ MP4 Video (Tech Rentals Showcase)
MP4_VIDEO_URL = "https://drive.google.com/uc?export=download&id=17SkstGw5ID0W7rxey_YuKQ8MusVcWHqI"

# ✅ Quotes Section
quotes = [
    "Technology is best when it brings people together. - Matt Mullenweg",
    "The best way to predict the future is to invent it. - Alan Kay",
    "Rent smarter, save money, and enjoy the latest tech!",
    "Why buy when you can rent? Gear up today!"
]
selected_quote = random.choice(quotes)

# ✅ Payment Methods
payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking"]

# ✅ Testimonials
testimonials = [
    {"name": "Amit Sharma", "review": "GearSpot made renting gadgets super easy! Highly recommend it."},
    {"name": "Sarah Khan", "review": "Loved the experience! I got a high-end laptop at a fraction of the cost."},
    {"name": "Rohan Verma", "review": "Fantastic service and great gadgets. Will rent again!"}
]

# ✅ Featured Gadgets
featured_gadgets = [
    {"name": "PlayStation 5 Pro", "image": "https://4kwallpapers.com/images/walls/thumbs_3t/19032.jpg"},
    {"name": "Canon EOS R5", "image": "https://s7d1.scene7.com/is/image/canon/5077C002_eos-r5-c_primary_clean?fmt=webp-alpha&wid=1600"},
    {"name": "Oculus Quest 2", "image": "https://about.fb.com/wp-content/uploads/2020/09/NRP-Facebook_Connect_Introducing_Oculus_Quest_2_the_Next_Generation_of_All-in-One_VR_Gaming_inline-oculus_quest_2_with_controllers.jpg"}
]

# ✅ Session State for Cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# ✅ Function to Display Available Gadgets for Rent
def display_gadgets_for_rent(search_query):
    """Displays available rental gadgets."""
    gadgets = pd.DataFrame({
        'Name': ["PlayStation 5 Pro", "Canon EOS R5", "Oculus Quest 2"],
        'Category': ["Console", "Camera", "VR Headset"],
        'Price/Day': [25, 15, 20],
        'Availability': ["Available", "Rented", "Available"],
        'Image': [
            "https://4kwallpapers.com/images/walls/thumbs_3t/19032.jpg",
            "https://s7d1.scene7.com/is/image/canon/5077C002_eos-r5-c_primary_clean?fmt=webp-alpha&wid=1600",
            "https://about.fb.com/wp-content/uploads/2020/09/NRP-Facebook_Connect_Introducing_Oculus_Quest_2_the_Next_Generation_of_All-in-One_VR_Gaming_inline-oculus_quest_2_with_controllers.jpg"
        ]
    })
    
    if search_query:
        gadgets = gadgets[gadgets['Name'].str.contains(search_query, case=False, na=False)]
    
    for _, row in gadgets.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['Image'], width=120)
            with col2:
                st.markdown(f"**{row['Name']}**  ")
                st.markdown(f"*Category:* {row['Category']}")
                st.markdown(f"*Price/Day:* ₹{row['Price/Day']}")
                st.markdown(f"*Availability:* {row['Availability']}")
                if row['Availability'] == "Available":
                    if st.button(f"Add to Cart - {row['Name']}", key=row['Name']):
                        st.session_state.cart.append({"Name": row['Name'], "Total": row['Price/Day']})
                        st.success(f"✅ {row['Name']} added to cart!")
            st.write("---")

# ✅ Function to List a Gadget for Rent
def list_gadget_for_rent():
    """Form to list a gadget for rent."""
    gadget_name = st.text_input("Gadget Name")
    category = st.selectbox("Category", ["Console", "Camera", "Laptop", "Drone", "VR Headset", "Other"])
    price = st.number_input("Price per Day (₹)", min_value=1, step=1)
    available_from = st.date_input("Available From", datetime.today())
    submit = st.button("List My Gadget for Rent")
    
    if submit and gadget_name:
        st.success(f"🎉 Your {gadget_name} has been listed successfully!")

# ✅ Header with Logo & Cart Button on Top Right
col1, col2 = st.columns([5, 1])
with col1:
    st.image(LOGO_URL, width=150)
    st.title("GearSpot 🚀")
    st.subheader("Your hub for renting and lending gadgets!")
with col2:
    if st.button("🛒 Cart"):
        st.session_state.show_cart = True

# ✅ Display Hosted MP4 Video
st.markdown("## 🎥 Explore How GearSpot Works")
st.video(MP4_VIDEO_URL)

# ✅ Separate Pages for Renting & Lending
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📢 Rent a Gadget", "💼 Lend Your Gadget"])

if page == "🏠 Home":
    st.markdown(f"## ✨ Inspiration of the Day")
    st.markdown(f"### *{selected_quote}*")
    st.markdown("## 🔥 Featured Gadgets")
    cols = st.columns(len(featured_gadgets))
    for idx, gadget in enumerate(featured_gadgets):
        with cols[idx]:
            st.image(gadget["image"], width=250)
            st.markdown(f"**{gadget['name']}**")
    st.markdown("## ⭐ Customer Testimonials")
    for testimonial in testimonials:
        with st.container():
            st.markdown(f"**{testimonial['name']}**")
            st.markdown(f"*\"{testimonial['review']}\"*")
            st.write("---")

elif page == "📢 Rent a Gadget":
    st.subheader("📢 Available Gadgets for Rent")
    search_query = st.text_input("Search for a Gadget")
    display_gadgets_for_rent(search_query)

elif page == "💼 Lend Your Gadget":
    st.subheader("💼 List Your Gadget for Lending")
    list_gadget_for_rent()
