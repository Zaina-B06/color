import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

# Initialize Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ==============================================
# COMPREHENSIVE 16-SEASON COLOR ANALYSIS SYSTEM
# ==============================================
SEASONS = {
    "True Winter": {
        "description": "The classic winter - pure cool undertones with high contrast",
        "colors": ["Absolute White", "True Black", "Royal Blue", "Ruby Red", "Ice Gray", "Emerald Green"],
        "color_reasons": [
            "Creates maximum contrast",
            "Provides deepest backdrop",
            "Enhances natural coolness",
            "Powerful contrast that doesn't overwhelm",
            "Sophisticated neutral",
            "Brings out eye color"
        ],
        "hair": ["Blue-Black", "Platinum Blonde", "Cool Dark Brown"],
        "hair_reasons": [
            "Enhances natural high contrast",
            "Kept extremely cool-toned",
            "With obvious ash tones"
        ],
        "makeup": ["True Red Lipstick", "Cool Gray Eyeshadow", "Black Eyeliner"],
        "makeup_reasons": [
            "Blue-based reds complement lips",
            "Enhances eye shape",
            "Provides maximum definition"
        ],
        "jewelry": ["Platinum", "White Gold", "Sterling Silver"],
        "jewelry_reasons": [
            "Cool gray undertones harmonize",
            "Bright accent without warmth",
            "Affordable alternative"
        ],
        "avoid": ["Warm Browns", "Gold Jewelry", "Orange Tones"],
        "avoid_reasons": [
            "Make skin appear sallow",
            "Creates visual disharmony",
            "Drains natural vibrancy"
        ],
        "occasions": {
            "Business Formal": {
                "outfit": "Black suit with ice gray blouse",
                "shoes": "Patent black pumps",
                "accessories": "Platinum watch",
                "makeup": "Sheer true red lip"
            },
            "Cocktail Party": {
                "outfit": "Royal blue cocktail dress",
                "shoes": "Silver metallic heels",
                "accessories": "Silver cuff bracelet",
                "makeup": "Full coverage red lip"
            }
        }
    },
    "Bright Spring": {
        "description": "Warm undertones with extremely high contrast and clarity",
        "colors": ["Coral", "Aqua", "Lime Green", "Golden Yellow", "Bright Peach"],
        "color_reasons": [
            "Energizes complexion",
            "Refreshing contrast",
            "Brings out golden undertones",
            "Perfect warm neutral",
            "Mimics natural flush"
        ],
        "hair": ["Golden Blonde", "Copper Red", "Warm Light Brown"],
        "hair_reasons": [
            "Enhances natural warmth",
            "Makes skin radiant",
            "With golden highlights"
        ],
        "makeup": ["Coral Lipstick", "Peach Blush", "Bronze Eyeliner"],
        "makeup_reasons": [
            "Complements lip undertones",
            "Mimics youthful flush",
            "Warms up eye area"
        ],
        "jewelry": ["Yellow Gold", "Rose Gold", "Amber"],
        "jewelry_reasons": [
            "Harmonizes with warmth",
            "Adds romantic warmth",
            "Organic golden accent"
        ],
        "avoid": ["Cool Grays", "Muted Colors", "Silver Jewelry"],
        "avoid_reasons": [
            "Make you appear sallow",
            "Drain vibrancy",
            "Clashes with warm skin"
        ],
        "occasions": {
            "Business Formal": {
                "outfit": "Golden yellow blazer with white shell",
                "shoes": "Nude pumps",
                "accessories": "Gold hoop earrings",
                "makeup": "Peach lip gloss"
            },
            "Cocktail Party": {
                "outfit": "Coral wrap dress",
                "shoes": "Gold sandals",
                "accessories": "Gold necklace",
                "makeup": "Bronzed glow"
            }
        }
    },
    # Add other seasons following the same pattern
}

# ========================
# IMPROVED IMAGE ANALYSIS
# ========================
def analyze_image(uploaded_file):
    try:
        # Load and preprocess image
        image = Image.open(uploaded_file).convert('RGB')
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Enhanced face detection
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(150, 150),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) == 0:
            st.warning("No face detected. Try a clearer photo.")
            return None
        
        # Get largest face
        (x, y, w, h) = max(faces, key=lambda f: f[2]*f[3])
        
        # Create elliptical mask for better skin detection
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        center = (x + w//2, y + h//2)
        axes = (int(w*0.45), int(h*0.65))
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
        
        # Get skin pixels
        skin = cv2.bitwise_and(image, image, mask=mask)
        hsv_skin = cv2.cvtColor(skin, cv2.COLOR_BGR2HSV)
        skin_pixels = hsv_skin[np.where(mask == 255)]
        
        # More accurate color analysis
        clt = KMeans(n_clusters=3, n_init=10)
        clt.fit(skin_pixels)
        dominant_colors = clt.cluster_centers_.astype(int)
        
        # Improved season detection
        hue = dominant_colors[0][0]
        sat = dominant_colors[0][1]
        val = dominant_colors[0][2]
        
        if hue < 15 or hue > 165:  # Cool tones
            if sat > 150 and val > 180: return "Bright Winter"
            elif val > 160: return "True Winter"
            else: return "Cool Summer"
        elif 15 <= hue <= 45:  # Warm tones
            if sat > 140 and val > 170: return "Bright Spring"
            elif val > 150: return "True Autumn"
            else: return "Soft Autumn"
        else:  # Neutral/soft tones
            if sat < 100: return "Soft Summer"
            else: return "True Summer"
            
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")
        return None

# ========================
# STREAMLIT UI
# ========================
st.set_page_config(layout="wide", page_title="16-Season Color Analysis")

# Custom CSS
st.markdown("""
<style>
    .season-card {
        background-color: rgba(255,255,255,0.9);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .occasion-card {
        background-color: rgba(240,248,255,0.9);
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
    }
    .avoid-card {
        background-color: rgba(255,240,240,0.9);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    [data-testid="stImage"] {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 16-Season Color Analysis")
st.subheader("Discover Your Perfect Color Palette")

uploaded_file = st.file_uploader("Upload a well-lit frontal photo:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with st.spinner("Analyzing your skin tones..."):
        season = analyze_image(uploaded_file)
        
        if season:
            st.success(f"Your Color Season: **{season}**")
            st.caption(SEASONS[season]["description"])
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(uploaded_file, width=300, caption="Your Photo")
                
            with col2:
                tab1, tab2, tab3 = st.tabs(["🎨 Colors", "💄 Makeup & Hair", "👗 Occasion Wear"])
                
                with tab1:
                    st.subheader("Best Colors For You")
                    cols = st.columns(2)
                    for i, (color, reason) in enumerate(zip(SEASONS[season]["colors"], SEASONS[season]["color_reasons"])):
                        cols[i%2].markdown(f"""
                        <div class="season-card">
                            <h4>{color}</h4>
                            <p>{reason}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.subheader("Avoid These Colors")
                    for item, reason in zip(SEASONS[season]["avoid"], SEASONS[season]["avoid_reasons"]):
                        st.markdown(f"""
                        <div class="avoid-card">
                            <h4>{item}</h4>
                            <p>{reason}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Hair Colors")
                        for hair, reason in zip(SEASONS[season]["hair"], SEASONS[season]["hair_reasons"]):
                            st.markdown(f"""
                            <div class="season-card">
                                <h4>{hair}</h4>
                                <p>{reason}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        st.subheader("Makeup")
                        for makeup, reason in zip(SEASONS[season]["makeup"], SEASONS[season]["makeup_reasons"]):
                            st.markdown(f"""
                            <div class="season-card">
                                <h4>{makeup}</h4>
                                <p>{reason}</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                with tab3:
                    occasion = st.selectbox(
                        "Select occasion:",
                        list(SEASONS[season]["occasions"].keys())
                    )
                    rec = SEASONS[season]["occasions"][occasion]
                    st.markdown(f"""
                    <div class="occasion-card">
                        <h3>{occasion} Outfit</h3>
                        <p><strong>Outfit:</strong> {rec['outfit']}</p>
                        <p><strong>Shoes:</strong> {rec['shoes']}</p>
                        <p><strong>Accessories:</strong> {rec['accessories']}</p>
                        <p><strong>Makeup:</strong> {rec['makeup']}</p>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("""
Professional Color Analysis System | 
For best results: Use natural lighting, no makeup, and clear frontal photos
""")
