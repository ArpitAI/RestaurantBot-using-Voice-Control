
from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import time
import tempfile # Added for temporary file handling

# For Speech Recognition
import speech_recognition as sr

# For Text-to-Speech
from gtts import gTTS
# import io # Not strictly needed with tempfile approach, but harmless

# Configure Google Generative AI
# Robust API key loading for both local (.env) and deployed (st.secrets) environments
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except AttributeError:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except KeyError:
    st.error("API key not found. Please set GOOGLE_API_KEY in your .env file or Streamlit secrets.")
    st.stop()


## Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question, context=""):
    # If context is provided, prepend it to the question
    if context:
        full_question = f"Based on the following information: {context}\n\nUser query: {question}"
    else:
        full_question = question
    
    response = chat.send_message(full_question, stream=True)
    return response

# Function to convert text to speech and play - MODIFIED FOR LANGUAGE
def text_to_speech(text, lang='en'): # Added lang parameter with default 'en'
    if text:
        try:
            tts = gTTS(text=text, lang=lang) # Use the provided lang parameter

            # Create a temporary file to save the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_audio_path = fp.name
                tts.save(temp_audio_path)
            
            # Now, pass the path to the temporary file to st.audio
            st.audio(temp_audio_path, format="audio/mp3", start_time=0, autoplay=True)

            # Clean up the temporary file after Streamlit has had a chance to load it
            time.sleep(0.5) # Give Streamlit a moment to process the file
            os.remove(temp_audio_path)

        except Exception as e:
            st.error(f"Error converting text to speech in '{lang}': {e}") # Include lang in error
            st.warning("Speech output might not auto-play or work if there's an internet issue or browser policy.")


# --- Restaurant Documents (KEEP THESE AS IS) ---
# Note: For multi-language support with RAG, your documents should ideally also be
# available in the languages you support, or your LLM should be able to translate
# the query to English before RAG and then translate the answer back to Hindi.
# For simplicity, we'll assume the LLM can handle cross-lingual understanding
# with the English documents for now, or that the user sticks to one language.
Document1 = """Our restaurant is called "The Golden Spoon." We are located at 123 Main Street in Varanasi, Uttar Pradesh. You can reach us by phone at our landline 0542-6543210 or mobile at +91-9876543210. Our website is www.thegoldenspoon.com. We offer limited street parking. The main entrance and dining area are wheelchair accessible. We have a charming outdoor seating area during pleasant weather. We specialize in authentic North Indian cuisine with a modern twist, but also offer a wide range of international dishes. Ask us about our daily specials!"""

Document2 = """Welcome to The Golden Spoon in Varanasi! We offer a diverse menu featuring the best of Indian, Chinese, Continental, South Indian, Italian, Mexican, American, Australian, and Korean cuisines, alongside a selection of popular Indian Street Food & Chaat. Our opening hours are from 11:00 AM to 11:00 PM daily. For reservations or inquiries, please call us at 0542-6543210 or +91-9876543210, or visit our website at www.thegoldenspoon.com.

**Our Menu:**

**Indian Delights:**
* Samosa (2 Pcs - ₹80) - Vegetarian
* Chole Bhature (₹180) - Vegetarian
* Creamy Butter Chicken (₹380)
* Rich Paneer Tikka Masala (₹350) - Vegetarian
* Fragrant Chicken Biryani (₹420)
* Aromatic Mutton Biryani (₹480)
* Flavorful Vegetable Biryani (₹320) - Vegetarian, Vegan option available
* Flavorful Dal Makhani (₹300) - Vegan option available upon request
* Spicy Chana Masala (₹280) - Vegan
* Goan Fish Curry (₹450)
* Mutton Rogan Josh (₹480)
* Prawn Malai Curry (₹520)
* Mushroom Do Pyaza (₹320) - Vegetarian
* Palak Paneer (Spinach with Cottage Cheese - ₹340) - Vegetarian
* Aloo Gobi (Potato and Cauliflower Curry - ₹290) - Vegan
* Baingan Bharta (Roasted Eggplant Mash - ₹300) - Vegan
* Mix Vegetable Korma (₹310) - Vegetarian
* Shahi Paneer (₹360) - Vegetarian
* Naan (₹50), Garlic Naan (₹60), Butter Roti (₹35), Laccha Paratha (₹70)

**Chinese Favorites:**
* Chicken Manchurian (dry/gravy - ₹320)
* Vegetable Fried Rice (₹250) - Vegan option available
* Hakka Noodles (₹280) - Vegan option available
* Schezwan Chicken (₹350)
* Spring Rolls (Vegetable - ₹180 for 2, Chicken - ₹220 for 2) - Vegan option available for veg
* Kung Pao Chicken (₹360)
* Sweet and Sour Vegetables (₹290) - Vegan
* Chilli Paneer Dry (₹300) - Vegetarian
* Prawns in Hot Garlic Sauce (₹450)
* Mushroom in Black Bean Sauce (₹330) - Vegan
* Vegetable Manchurian Dry (₹280) - Vegan
* **Chowmein Varieties:**
    * Vegetable Chowmein (₹280) - Vegan option available
    * Chicken Chowmein (₹300)
    * Egg Chowmein (₹290)
    * Mixed Chowmein (Chicken & Egg) (₹320)
    * Paneer Chowmein (₹300) - Vegetarian

**Continental Selection:**
* Grilled Chicken with Mushroom Sauce (₹400)
* Fish and Chips (₹380)
* Shepherd's Pie (₹360)
* Vegetable Au Gratin (₹320) - Vegetarian
* Chicken Stroganoff (₹420)
* Creamy Chicken Alfredo (₹400)
* Pan-Seared Salmon with Lemon-Dill Sauce (₹550)
* Roasted Vegetable Lasagna (₹390) - Vegetarian
* Mushroom Risotto (₹380) - Vegetarian
* Vegan Shepherd's Pie (Lentil and Vegetable - ₹360) - Vegan
* Potato Wedges with Dip (₹180) - Vegetarian, Vegan

**South Indian Specialties:**
* **Idli with Sambar & Chutneys:**
    * Plain Idli (2 Pcs) - ₹100 (Vegan)
    * Fried Idli (2 Pcs) - ₹120 (Vegan)
    * Podi Idli (2 Pcs) - ₹130 (Vegan)
    * Rava Idli (2 Pcs) - ₹110 (Vegetarian)
* **Dosa (served with Sambar & Chutneys):**
    * Plain Dosa - ₹120 (Vegan)
    * Masala Dosa (Potato filling) - ₹180 (Vegan)
    * Paneer Dosa - ₹220 (Vegetarian)
    * Rava Dosa (Crispy Semolina Dosa) - ₹160 (Vegan)
    * Onion Rava Dosa - ₹180 (Vegan)
    * Mysore Masala Dosa (Spicy Red Chutney, Potato filling) - ₹200 (Vegan)
    * Cheese Dosa - ₹250 (Vegetarian)
    * Ghee Roast Dosa - ₹150 (Vegetarian)
    * Mushroom Dosa - ₹200 (Vegetarian)
    * Paper Roast Dosa - ₹130 (Vegan)
    * Set Dosa (Soft, spongy dosas, 2 pcs) - ₹150 (Vegan)
* **Uttapam (Thick Savory Pancakes):**
    * Plain Uttapam - ₹140 (Vegan)
    * Onion Uttapam - ₹160 (Vegan)
    * Tomato Uttapam - ₹160 (Vegan)
    * Mixed Vegetable Uttapam - ₹180 (Vegan)
    * Paneer Uttapam - ₹220 (Vegetarian)
    * Corn Uttapam - ₹190 (Vegetarian)
* Savory Vada (2 Pcs) - ₹100 (Vegan)
* Tangy Pongal - ₹160 (Vegan)
* South Indian Thali (Assortment of regional specialties) - ₹300 (Vegan option available)
* Curd Rice - ₹150 (Vegetarian)
* Lemon Rice - ₹160 (Vegan)
* Vegetable Upma - ₹140 (Vegan)

**Street Food & Chaat (Available from 4:00 PM onwards):**
* **Golgappe / Pani Puri (6 Pcs):**
    * Classic Golgappe - ₹80 (Vegan)
    * Dahi Golgappe (with yogurt) - ₹100 (Vegetarian)
* **Chaat Varieties:**
    * Aloo Tikki Chaat (Potato patties with chutneys & yogurt) - ₹150 (Vegetarian)
    * Papdi Chaat (Crispy fried dough with chutneys & yogurt) - ₹140 (Vegetarian)
    * Dahi Bhalla (Lentil fritters in yogurt) - ₹160 (Vegetarian)
    * Samosa Chaat - ₹130 (Vegetarian)
    * Pav Bhaji (Mixed vegetable mash with buttered bun) - ₹200 (Vegetarian, Vegan option available)
    * Vada Pav (Spiced potato fritter in a bun) - ₹100 (Vegetarian, Vegan option available)
* Bhel Puri (Puffed rice salad) - ₹120 (Vegan)
* Sev Puri (Crispy flatbread with toppings) - ₹130 (Vegetarian)

**Italian Indulgence:**
* Margherita Pizza (₹350 for 10 inch) - Vegan cheese option available
* Creamy Alfredo Pasta (with chicken - ₹400, with vegetables - ₹350) - Vegan Alfredo option available
* Spicy Arrabbiata Pasta (₹320) - Vegan
* Cheesy Lasagna (₹450) - Vegetarian option available
* Flavorful Mushroom Risotto (₹380) - Vegetarian
* Garlic Bread (₹120 for 4 slices) - Vegan option available
* Pepperoni Pizza (₹450 for 10 inch)
* Spaghetti Carbonara (₹420)
* Vegan Pizza with Roasted Vegetables (₹380 for 10 inch) - Vegan
* Focaccia Bread with Herbs (₹150) - Vegan

**Mexican Fiesta:**
* Chicken Quesadilla (₹380)
* Vegetable Burrito Bowl (₹320) - Vegan option available
* Nachos with Salsa and Guacamole (₹280) - Vegan option available
* Tacos (Chicken - ₹150, Paneer - ₹150, Mushroom & Bean - ₹140 per piece) - Vegan option for Mushroom & Bean
* Enchiladas (Veg - ₹380, Chicken - ₹420) - Vegan option for veg
* Fajita Platter (Sizzling Vegetables - ₹400, Chicken - ₹450) - Vegan option for veg

**American Classics:**
* Classic Beef Burger with Fries (₹450)
* Crispy Chicken Burger (₹400)
* BBQ Ribs (₹600)
* Mac and Cheese (₹300) - Vegetarian
* Caesar Salad with Grilled Chicken (₹350) - Vegan Caesar dressing option available
* Pulled Pork Sandwich (₹480)
* Vegan Black Bean Burger (₹380) - Vegan
* Onion Rings (₹190) - Vegetarian, Vegan

**Australian Outback:**
* Australian Lamb Chops (₹700)
* Barramundi Fillet with Roasted Vegetables (₹600)
* Chicken Parma (₹480)
* Pavlova (Dessert - ₹250) - Vegetarian
* Vegan Lamingtons (₹180 for 2) - Vegan

**Korean Delights:**
* Kimchi Jjigae (Spicy Kimchi Stew with Tofu/Pork) - ₹400 (Vegetarian/Vegan option with Tofu)
* Bibimbap (Mixed Rice with Vegetables & Egg/Meat) - ₹450 (Vegetarian/Vegan option available)
* Korean Fried Chicken (Crispy Fried Chicken with Gochujang Sauce) - ₹480
* Tteokbokki (Spicy Rice Cakes) - ₹350 (Vegetarian, Vegan option available)
* Japchae (Stir-fried Glass Noodles with Vegetables) - ₹320 (Vegetarian, Vegan)
* Bulgogi (Marinated Grilled Beef) - ₹550
* Kimchi Pancake (Kimchi Jeon) - ₹280 (Vegetarian, Vegan)
* Gyeran-jjim (Steamed Egg Custard) - ₹200 (Vegetarian)

**Beverages:**
* Soft Drinks (₹60), Fresh Juices (Orange, Watermelon, Pineapple - ₹80)
* Lassi (Sweet/Salted - ₹90, Mango - ₹120, Rose - ₹100)
* Masala Chai (₹50), Hot Coffee (₹70), Cold Coffee (₹90)
* Fresh Lime Soda (₹80)
* Vegan Milkshakes (Almond Milk Chocolate/Vanilla - ₹150)
* Korean Barley Tea (Iced/Hot) - ₹90

**Desserts:**
* Gulab Jamun (₹80 for 2), Rasgulla (₹70 for 2)
* Chocolate Lava Cake (₹200)
* Ice Cream (Vanilla, Chocolate, Strawberry, Pista - ₹100 per scoop) - Vegan sorbet option available
* Tiramisu (₹220) - Vegetarian
* Fresh Fruit Platter (₹180) - Vegan
* Kulfi (Mango, Pista - ₹120) - Vegetarian
* Bingsu (Korean Shaved Ice Dessert - seasonal) - ₹300

**Vegetarian & Vegan Options:** We have a wide array of delicious vegetarian and vegan options across all cuisines, clearly marked on our in-house and online menus. Look for the (V) for Vegetarian and (VG) for Vegan symbols on our menu, or ask your server for assistance.

**Allergies:** Please inform your server of any dietary restrictions or allergies, and our staff will be happy to assist you. Enjoy your dining experience at The Golden Spoon! We appreciate your patronage."""

Document3 = """Yes, we do offer home delivery within a 5-kilometer radius of our restaurant. You can place your order by calling us directly at +91-9876543210 (mobile) or our landline 0542-6543210. The minimum order for delivery is ₹300. Our delivery charges are ₹50 for orders below ₹500 and free for orders above ₹500. The estimated delivery time is typically 30-45 minutes, depending on the distance and order volume. You can customize most dishes; please specify your requests when placing your order (e.g., "no onions," "extra spicy," "vegan cheese"). We accept online payments (UPI, Net Banking, major credit/debit cards), credit/debit cards upon delivery, and cash on delivery. Gift cards can be redeemed for both dine-in and delivery orders. To inquire about the status of your delivery or to request a cancellation (within a reasonable timeframe before dispatch), please call us immediately at +91-9876543210."""

Document4 = """Yes, we highly recommend making a reservation, especially during peak hours and weekends. You can make a reservation through our website at www.thegoldenspoon.com/reservations or by calling us at 0542-6543210 or +91-9876543210. The earliest reservation we typically take is for our opening time, and the latest is one hour before closing. You can reserve a table for up to 10 people online. For larger parties or special events, please call us directly. While we try our best to accommodate requests for specific tables, it cannot be guaranteed. The standard table reservation time is 1.5 to 2 hours, depending on the party size. To modify or cancel your reservation, please do so at least 2 hours in advance via our website or by phone."""

Document5 = """Our goal is to provide a delicious and satisfying dining experience. We use fresh, flavorful, and quality ingredients in all our dishes. Our chefs ensure that each meal is well-cooked and presented beautifully. If, for any reason, you find your food to be undercooked, overcooked, bland, or not to your satisfaction, please inform your server immediately, and we will do our best to rectify the situation. We may offer a replacement dish, a discount on your current meal, or a complimentary item as compensation, depending on the issue. We strive for friendly, attentive, and efficient service. If you experience slow or rude service, please speak to your manager immediately so we can address it. We aim to create a cozy and comfortable ambiance with tasteful decor and background music. We believe our prices offer reasonable value for the quality of food and service provided. If you have any complaints or feedback regarding your overall experience, please don't hesitate to share it with our staff or leave a review on our website or other platforms."""

Document6 = """We take dietary needs and allergies seriously. Please inform your server about any vegetarian, vegan, or gluten-free requirements or any specific allergies, such as nut, dairy, soy, or shellfish allergies. Our staff is trained to handle special requests and can guide you through the menu options that are suitable for you. We also have a separate allergen menu available upon request. While we take utmost precautions to avoid cross-contamination, please be aware that our kitchen handles various allergens. We aim for order accuracy and sincerely apologize if you receive a wrong order or a missing item. Please notify us immediately, and we will promptly correct your order. For delivery experiences, we strive for on-time delivery and ensure that food is properly packaged to maintain temperature and quality. If your delivery is late, or if you receive cold food or damaged packaging, please contact us at +91-9876543210, and we will address your concerns and may offer a partial refund or a complimentary item on your next order as a gesture of goodwill."""

Document7 = """Our kitchen maintains a diverse stock of fresh produce, various meats (chicken, lamb, fish, prawns, beef), dairy products, plant-based alternatives (tofu, tempeh, vegan cheeses, almond milk), grains (rice, pasta), and a wide array of spices and beverages to ensure we can prepare all our menu items. We regularly monitor our stock levels to avoid running out of ingredients. We work with trusted local farmers and reputable suppliers to order and purchase high-quality ingredients, and we maintain detailed invoices for all purchases to ensure traceability. Our storage facilities include state-of-the-art refrigeration, freezers, and dry storage areas to maintain the freshness and quality of all our ingredients. We adhere to strict shelf life guidelines and manage our inventory through a 'first-in, first-out' system to minimize spoilage and waste through careful portion control and demand forecasting. We have a robust system in place for tracking our inventory, including regular counts and audits to ensure efficiency and freshness."""

Document8 = """We continuously strive to streamline our processes for efficiency and enhance the customer experience. Our advanced order management system ensures quick processing and accurate fulfillment of both dine-in and delivery orders. Our kitchen utilizes a sophisticated kitchen display system (KDS) to optimize workflow, synchronize meal preparation, and ensure timely delivery of hot food. For table management, our seating arrangements are designed for optimal flow and comfort, and we use a modern reservation system to efficiently manage bookings and waitlists, reducing customer waiting times. We offer various convenient payment processing options, including secure online payments, contactless card payments through our point of sale (POS) system, and cash payments. Efficient internal and staff communication is crucial for smooth operations, facilitated by internal messaging systems and daily briefings. We are actively exploring opportunities for automation, such as automated online ordering, digital menus accessible via QR codes, and AI-powered customer service tools. Our overall workflow is designed with clear steps and seamless coordination among all team members, from kitchen staff to servers and management, ensuring a cohesive and efficient dining experience. We leverage technology and integrate various software platforms to enhance our operational efficiency and customer satisfaction."""

Document9 = """We often have special offers and exciting promotions for our valued customers. Please check our website (www.thegoldenspoon.com/offers) or ask your server about our current deals and discounts, which might include seasonal specials or combo offers. We also have a popular happy hour from 5 PM to 7 PM daily, featuring discounted beverages and appetizers. Yes, we proudly host private events and offer extensive catering services for all occasions, from intimate gatherings to large corporate events. Our catering options are highly flexible and can be fully customized to suit your specific dietary needs, preferences, and budget. Please contact our dedicated events coordinator at +91-9876543210 or email events@thegoldenspoon.com for more details and a personalized quote. We actively encourage our customers to leave feedback and reviews on our website and popular platforms like Google Reviews, Zomato, and TripAdvisor. Your ratings and comments are incredibly important to us, and we continuously strive to improve our services and offerings based on customer feedback. We are currently developing an exclusive loyalty program to reward our regular customers with points for every visit, which can be redeemed for discounts, free meals, and special access to events. Stay tuned for more information on how to earn points and redeem your golden rewards!"""

Document10 = """For specific allergen information about any dish, please ask your server, and they can provide you with detailed information from our comprehensive allergen menu. We are actively working on providing nutritional values for our menu items on our website soon, aiming for complete transparency. We are committed to sustainability and strive to minimize our environmental footprint by using eco-friendly packaging for our takeout and delivery orders whenever possible. We prioritize sourcing our ingredients locally whenever feasible to support local farmers, reduce our carbon footprint, and ensure the freshest produce for your meals. Our kitchen staff includes a team of highly experienced and passionate chefs who meticulously oversee the preparation of all dishes, ensuring quality and authenticity. Our friendly and attentive servers and waiters are here to provide excellent service at your table, ensuring a comfortable and enjoyable dining experience. Our welcoming hostess will greet you upon arrival and assist you with seating arrangements and any initial inquiries. The restaurant is managed by a dedicated team focused on ensuring a positive dining experience for every guest, from the moment you step in until you leave. Our skilled bartenders prepare a variety of refreshing beverages, from classic cocktails to freshly squeezed juices, at our well-stocked bar. Our kitchen is equipped with modern, high-efficiency equipment, including advanced ovens, precise stoves, efficient fryers, and a commercial dishwasher, all maintaining the highest standards of hygiene. We utilize a robust POS system for streamlined order taking and efficient payment processing, enhancing speed and accuracy."""

Document11 = """We value your feedback immensely and are always looking to improve! If you had a great experience, we'd love for you to share your positive comments and leave a review on our website (www.thegoldenspoon.com/reviews) or on Google Reviews, Zomato, or TripAdvisor. Your positive comments help us grow, motivate our dedicated team, and spread the word about The Golden Spoon. If, for any reason, you are not satisfied with your food or service, please let us know immediately while you are at the restaurant, so we can rectify the situation on the spot. If you've already left, please call us at +91-9876543210 (mobile) or 0542-6543210 (landline) within 24 hours of your visit or delivery. We sincerely apologize if our food or service did not meet your expectations. Could you please tell us more about what specifically was not to your liking (e.g., taste, temperature, cooking level, specific service issue)? We take all feedback seriously and use it to enhance our offerings. As a token of our apology and commitment to your satisfaction, we would like to offer you a complimentary dessert on your next visit, a discount on your next home delivery order, or a gift voucher for a future meal, depending on the nature of the issue. Our aim is to ensure every customer has a truly golden and delightful dining experience with us."""

documents = [Document1, Document2, Document3, Document4, Document5, Document6, Document7, Document8, Document9, Document10, Document11]


# --- ChromaDB Setup ---
class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True

    def __call__(self, input: Documents) -> Embeddings:
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        response = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type=embedding_task,
        )
        return response["embedding"]

DB_NAME = "googlerestaurentdb"
embed_fn = GeminiEmbeddingFunction()

# Initialize ChromaDB client and get or create collection
chroma_client = chromadb.Client()
db = chroma_client.get_or_create_collection(name=DB_NAME, embedding_function=embed_fn)

# Add documents to ChromaDB if not already present
if db.count() == 0:
    print("Adding documents to ChromaDB...")
    db.add(documents=documents, ids=[f"doc{i}" for i in range(len(documents))])
    print("Documents added.")
else:
    print("ChromaDB already populated.")

# --- Streamlit UI ---
st.set_page_config(page_title="The Golden Spoon Chatbot", layout="centered", initial_sidebar_state="auto")

# --- Title and Header ---
st.title("✨ The Golden Spoon Chatbot")
st.markdown("---") # A horizontal line for visual separation

# --- Language Selection (NEW) ---
# Initialize session state for language if not already set
if 'selected_language' not in st.session_state:
    st.session_state['selected_language'] = 'en' # Default to English

st.sidebar.subheader("Language Selection")
language_options = {
    "English": "en",
    "हिंदी (Hindi)": "hi"
}
selected_lang_name = st.sidebar.radio(
    "Choose your language:",
    options=list(language_options.keys()),
    index=0 if st.session_state['selected_language'] == 'en' else 1
)
# Update session state if selection changes
if language_options[selected_lang_name] != st.session_state['selected_language']:
    st.session_state['selected_language'] = language_options[selected_lang_name]
    st.rerun() # Rerun to apply language change immediately

# --- Chat History Initialization ---
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- Display Chat Messages ---
st.subheader("Conversation")
for role, text in st.session_state['chat_history']:
    with st.chat_message(role.lower()):
        st.write(text)

# --- User Input Section (Modified for Voice Input) ---
current_turn_user_input = None

voice_input_placeholder = st.empty()
text_input_placeholder = st.empty()

# The voice input button should always be available.
with voice_input_placeholder.container():
    st.subheader("Input Options")
    if st.button("🎤 Speak Now"):
        with st.spinner("Listening..."):
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    st.info(f"Say something in {selected_lang_name}!")
                    audio = r.listen(source, timeout=5)
                
                # Recognize speech in the selected language
                # Google Speech Recognition language codes: 'en-US' for English, 'hi-IN' for Hindi
                lang_code_for_sr = 'hi-IN' if st.session_state['selected_language'] == 'hi' else 'en-US'
                recognized_speech = r.recognize_google(audio, language=lang_code_for_sr)
                st.session_state['temp_user_input'] = recognized_speech
                
                st.rerun() 

            except sr.UnknownValueError:
                st.error("Sorry, I could not understand your audio. Please try again.")
                st.session_state['temp_user_input'] = None
            except sr.WaitTimeoutError:
                st.warning("No speech detected. Please speak clearly.")
                st.session_state['temp_user_input'] = None
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; check your internet connection: {e}")
                st.session_state['temp_user_input'] = None
            except Exception as e:
                st.error(f"An unexpected error occurred with speech recognition: {e}. "
                         "Please ensure your microphone is connected and permissions are granted.")
                st.session_state['temp_user_input'] = None

with text_input_placeholder.container():
    typed_user_input = st.chat_input("Or type your question here...", key="text_input_main")

if current_turn_user_input is None: # Only pick from temp_user_input or typed_user_input if not already set
    if st.session_state.get('temp_user_input'):
        current_turn_user_input = st.session_state.pop('temp_user_input')
    elif typed_user_input:
        current_turn_user_input = typed_user_input

if current_turn_user_input:
    # Add user query to chat history
    st.session_state['chat_history'].append(("User", current_turn_user_input))

    # Display user message
    with st.chat_message("user"):
        st.write(current_turn_user_input)

    # Search ChromaDB for relevant context
    # Note: ChromaDB with current setup is English-centric.
    # For robust multilingual RAG, you might need a multilingual embedding model
    # or translation steps before/after RAG.
    embed_fn.document_mode = False 
    result = db.query(query_texts=[current_turn_user_input], n_results=1)
    
    context_document = ""
    if result["documents"] and result["documents"][0]:
        context_document = result["documents"][0][0]
        # print(f"Retrieved Context: {context_document}") # Uncomment for debugging

    # Get Gemini response with context
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Instruct Gemini to respond in the selected language
        language_instruction = ""
        if st.session_state['selected_language'] == 'hi':
            language_instruction = "कृपया हिन्दी में उत्तर दें। " # Please answer in Hindi.
        
        # Pass the retrieved context and language instruction to the Gemini model
        for chunk in get_gemini_response(f"{language_instruction}{current_turn_user_input}", context_document):
            full_response += chunk.text + " "
            message_placeholder.write(full_response + "▌")
            time.sleep(0.05)

        final_assistant_response = full_response.strip()
        message_placeholder.write(final_assistant_response)
        st.session_state['chat_history'].append(("Assistant", final_assistant_response))
        
        # --- Voice Output Trigger (Backend Logic) ---
        # Convert assistant's response to speech in the selected language
        text_to_speech(final_assistant_response, lang=st.session_state['selected_language'])

        # Clear the text input box after processing (if input came from text)
        if typed_user_input:
            st.rerun() 


# --- Clear Chat History Button (Optional) ---
if st.session_state['chat_history']:
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state['chat_history'] = []
        st.rerun()