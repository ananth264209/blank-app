import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ✅ Set Page Config First
st.set_page_config(page_title="GearSpot - Rent & Lend Gadgets", layout="wide")
import os

VISIT_COUNTER_FILE = "visit_count.txt"

# Initialize file if it doesn't exist
if not os.path.exists(VISIT_COUNTER_FILE):
    with open(VISIT_COUNTER_FILE, "w") as f:
        f.write("0")

# Read and increment the counter
with open(VISIT_COUNTER_FILE, "r") as f:
    visit_count = int(f.read().strip())

visit_count += 1

# Write the updated counter back
with open(VISIT_COUNTER_FILE, "w") as f:
    f.write(str(visit_count))

# Store in session to avoid multiple increments per session
if "has_counted" not in st.session_state:
    st.session_state.has_counted = True
    st.session_state.visit_count = visit_count
else:
    st.session_state.visit_count = visit_count

# ✅ Logo Link
LOGO_URL = "https://i.imghippo.com/files/BMC2958Qc.png"

# ✅ Large Banner Image (Only for Home Page)
BANNER_IMAGE = "https://w0.peakpx.com/wallpaper/425/617/HD-wallpaper-stone-wall-texture-cartoon-wall-background-purple-stone-background-stone-texture.jpg"

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
    {"name": "Prahlad", "review": "GearSpot made renting gadgets super easy! Highly recommend it."},
    {"name": "Anuj", "review": "Loved the experience! I got a high-end laptop at a fraction of the cost."},
    {"name": "Prasanna", "review": "Fantastic service and great gadgets. Will rent again!"}
]

# ✅ Initial Available Gadgets

if "available_gadgets" not in st.session_state:
    st.session_state.available_gadgets = pd.DataFrame({
        'Name': [
            "PlayStation 5",
            "Canon EOS R5",
            "Oculus Quest 2",
            "Dell Alienware",
            "Spiderman 2 PS5",
            "Uncharted Remastered PS5",
            "Marshall Emberton 2",
            "PS F1 Setup",
            "Garmin Fenix 7 Pro"
        ],
        'Category': [
            "Console",
            "Camera",
            "VR Headset",
            "Laptop",
            "Console",
            "Console",
            "Speaker",
            "Console Accessory",
            "Smartwatch"
        ],
        'Price/Day': [700, 550, 900, 650, 250, 150, 700, 1000, 600],
        'Availability': [
            "Available",
            "Rented",
            "Available",
            "Available",
            "Rented",
            "Available",
            "Rented",
            "Available",
            "Available"
        ],
        'Image': [
            "https://gmedia.playstation.com/is/image/SIEPDC/ps5-slim-edition-left-image-block-01-en-24jun24?$1600px--t$",
            "https://s7d1.scene7.com/is/image/canon/5077C002_eos-r5-c_primary_clean?fmt=webp-alpha&wid=1600",
            "https://about.fb.com/wp-content/uploads/2020/09/NRP-Facebook_Connect_Introducing_Oculus_Quest_2_the_Next_Generation_of_All-in-One_VR_Gaming_inline-oculus_quest_2_with_controllers.jpg",
            "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/alienware-notebooks/alienware-x14-r2-intel/media-gallery/notebook-alienware-x14-r2-gray-gallery-7.psd?fmt=png-alpha&pscan=auto&scl=1&wid=4091&hei=2437&qlt=100,1&resMode=sharp2&size=4091,2437&chrss=full&imwidth=5000",
            "https://i.imghippo.com/files/w9824it.png",
            "https://i.imghippo.com/files/WS1286ug.png",
            "https://i.imghippo.com/files/MtBU4822kNM.png",
            "https://i.imghippo.com/files/oZl7819EU.png",
            "https://i.imghippo.com/files/MIdD5194Ro.png"
        ]
    })

# ✅ Session State for Cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# ✅ Function to Display Available Gadgets in Card Format
def display_gadgets_for_rent(search_query):
    """Displays available rental gadgets in a card format with rental duration selection."""
    gadgets = st.session_state.available_gadgets

    if search_query:
        gadgets = gadgets[gadgets['Name'].str.contains(search_query, case=False, na=False)]

    for _, row in gadgets.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['Image'], width=150)
            with col2:
                st.markdown(f"### {row['Name']}")
                st.markdown(f"**Category:** {row['Category']}")
                st.markdown(f"**Price/Day:** ₹{row['Price/Day']}")
                st.markdown(f"**Availability:** {row['Availability']}")

                if row['Availability'] == "Available":
                    rental_days = st.number_input(f"Select Rental Duration (Days) for {row['Name']}", min_value=1, step=1, key=row['Name']+"_days")
                    total_price = row['Price/Day'] * rental_days
                    
                    if st.button(f"Add to Cart - {row['Name']}", key=row['Name']):
                        st.session_state.cart.append({"Name": row['Name'], "Days": rental_days, "Total": total_price})
                        st.success(f"✅ {row['Name']} added to cart for {rental_days} days! Total: ₹{total_price}")

            st.write("---")

# ✅ Function to Show the Cart
def show_cart():
    st.sidebar.title("🛒 Your Cart")
    
    if not st.session_state.cart:
        st.sidebar.info("Your cart is empty.")
        return
    
    total_price = sum(item["Total"] for item in st.session_state.cart)
    
    for idx, item in enumerate(st.session_state.cart):
        st.sidebar.markdown(f"**{item['Name']}** - {item['Days']} Days - ₹{item['Total']}")
        if st.sidebar.button(f"❌ Remove {item['Name']}", key=f"remove_{idx}"):
            del st.session_state.cart[idx]
            st.experimental_rerun()

    st.sidebar.markdown(f"### Total: ₹{total_price}")
    
    payment_method = st.sidebar.selectbox("Select Payment Method", payment_methods)

    # ✅ Proceed to Payment Logic
    if st.sidebar.button("Proceed to Payment"):
        st.session_state.payment_success = True
        st.session_state.cart.clear()

       



# ✅ Function to List a Gadget for Rent
def list_gadget_for_rent():
    """Form to list a gadget for rent."""
    gadget_name = st.text_input("Gadget Name")
    category = st.selectbox("Category", ["Console", "Camera", "Laptop", "Drone", "VR Headset", "Other"])
    price = st.number_input("Price per Day (₹)", min_value=1, step=1)
    available_from = st.date_input("Available From", datetime.today())
    image_url = st.text_input("Image URL (optional)")

    submit = st.button("List My Gadget for Rent")

    if submit and gadget_name:
        new_gadget = pd.DataFrame({
            'Name': [gadget_name],
            'Category': [category],
            'Price/Day': [price],
            'Availability': ["Available"],
            'Image': [image_url if image_url else "https://via.placeholder.com/150"]
        })
        
        st.session_state.available_gadgets = pd.concat([st.session_state.available_gadgets, new_gadget], ignore_index=True)
        st.success(f"🎉 Your {gadget_name} has been listed successfully!")

# ✅ Header with Logo & Cart Button on Top Right
col1, col2 = st.columns([5, 1])
with col1:
    st.image(LOGO_URL, width=150)
    st.title("GearSpot 🚀")
    st.subheader("Your hub for renting and lending gadgets!")
with col2:
    if st.button("🛒 Cart"):
        show_cart()

# ✅ Separate Pages for Renting & Lending
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📢 Rent a Gadget", "💼 Lend Your Gadget"])

if page == "🏠 Home":
    st.image(BANNER_IMAGE, use_container_width=True)
    st.markdown(f"## ✨ Inspiration of the Day")
    st.markdown(f"### *{selected_quote}*")
    st.markdown("## 🔥 Featured Gadgets")
    cols = st.columns(len(st.session_state.available_gadgets))
    for idx, row in st.session_state.available_gadgets.iterrows():
        with cols[idx % len(cols)]:
            st.image(row["Image"], width=250)
            st.markdown(f"**{row['Name']}**")
    st.markdown("## ⭐ Customer Testimonials")
    for testimonial in testimonials:
        with st.container():
            st.markdown(f"**{testimonial['name']}**")
            st.markdown(f"*\"{testimonial['review']}\"*")
            st.write("---")
    # ✅ Manual WhatsApp Order Link
    st.markdown("## 📲 Place Your Order via WhatsApp")

# Replace the below URL with your actual WhatsApp order link
    manual_whatsapp_link = "https://wa.me/917861864714?text=I'm%20ready%20to%20place%20my%20order%20on%20GearSpot!"

    st.markdown(
       f"[🟢 Click here to place your order on WhatsApp]({manual_whatsapp_link})",
       unsafe_allow_html=True
  )

    st.markdown("---")
    st.markdown(f"📈 **Total Site Visits:** `{st.session_state.visit_count}`") 

elif page == "📢 Rent a Gadget":
    st.subheader("📢 Available Gadgets for Rent")
    search_query = st.text_input("Search for a Gadget")
    display_gadgets_for_rent(search_query)

elif page == "💼 Lend Your Gadget":
    st.subheader("💼 List Your Gadget for Lending")
    list_gadget_for_rent()
    

# ✅ Trigger WhatsApp redirection after payment
if st.session_state.get("payment_success", False):
    st.success("✅ Payment Successful! Redirecting you to WhatsApp...")

    whatsapp_number = "919176376320"  # Replace with your number
    message = "Hi, I just completed my rental order on GearSpot! 📦"
    encoded_msg = message.replace(" ", "%20")
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={encoded_msg}"

    # JavaScript-based redirection (reliable)
    st.markdown(
        f"""
        <script>
            window.open("{whatsapp_link}", "_blank");
        </script>
        """,
        unsafe_allow_html=True
    )

    # Fallback clickable link
    st.markdown(f"[👉 Click here if you're not redirected automatically]({whatsapp_link})", unsafe_allow_html=True)

    # Reset the trigger
    st.session_state.payment_success = False
