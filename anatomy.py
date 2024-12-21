import streamlit as st
import random
from difflib import SequenceMatcher

# Adjusted bone list with unique entries
bones = [
    # Skull Bones
    {"name": "Frontal", "region": "Cranium", "type": "Flat"},
    {"name": "Parietal", "region": "Cranium", "type": "Flat"},
    {"name": "Temporal", "region": "Cranium", "type": "Irregular"},
    {"name": "Occipital", "region": "Cranium", "type": "Flat"},
    {"name": "Sphenoid", "region": "Cranium", "type": "Irregular"},
    {"name": "Ethmoid", "region": "Cranium", "type": "Irregular"},
    {"name": "Maxilla", "region": "Face", "type": "Irregular"},
    {"name": "Mandible", "region": "Face", "type": "Irregular"},
    {"name": "Zygomatic", "region": "Face", "type": "Irregular"},
    {"name": "Nasal", "region": "Face", "type": "Flat"},
    {"name": "Lacrimal", "region": "Face", "type": "Flat"},
    {"name": "Palatine", "region": "Face", "type": "Irregular"},
    {"name": "Vomer", "region": "Face", "type": "Flat"},
    {"name": "Inferior Nasal Concha", "region": "Face", "type": "Irregular"},
    {"name": "Malleus", "region": "Middle Ear", "type": "Irregular"},
    {"name": "Incus", "region": "Middle Ear", "type": "Irregular"},
    {"name": "Stapes", "region": "Middle Ear", "type": "Irregular"},
    {"name": "Hyoid", "region": "Neck", "type": "Irregular"},

    # Torso Bones
    {"name": "Cervical Vertebrae", "region": "Neck", "type": "Irregular"},
    {"name": "Thoracic Vertebrae", "region": "Upper Back", "type": "Irregular"},
    {"name": "Lumbar Vertebrae", "region": "Lower Back", "type": "Irregular"},
    {"name": "Sacrum", "region": "Pelvis", "type": "Irregular"},
    {"name": "Coccyx", "region": "Pelvis", "type": "Irregular"},
    {"name": "True Rib", "region": "Thorax", "type": "Flat"},
    {"name": "False Rib", "region": "Thorax", "type": "Flat"},
    {"name": "Floating Rib", "region": "Thorax", "type": "Flat"},
    {"name": "Manubrium", "region": "Thorax", "type": "Flat"},
    {"name": "Body of Sternum", "region": "Thorax", "type": "Flat"},
    {"name": "Xiphoid Process", "region": "Thorax", "type": "Flat"},

    # Upper Extremities
    {"name": "Clavicle", "region": "Shoulder", "type": "Long"},
    {"name": "Scapula", "region": "Shoulder", "type": "Flat"},
    {"name": "Humerus", "region": "Upper Arm", "type": "Long"},
    {"name": "Radius", "region": "Forearm", "type": "Long"},
    {"name": "Ulna", "region": "Forearm", "type": "Long"},
    {"name": "Scaphoid", "region": "Wrist", "type": "Short"},
    {"name": "Lunate", "region": "Wrist", "type": "Short"},
    {"name": "Triquetrum", "region": "Wrist", "type": "Short"},
    {"name": "Pisiform", "region": "Wrist", "type": "Short"},
    {"name": "Trapezium", "region": "Wrist", "type": "Short"},
    {"name": "Trapezoid", "region": "Wrist", "type": "Short"},
    {"name": "Capitate", "region": "Wrist", "type": "Short"},
    {"name": "Hamate", "region": "Wrist", "type": "Short"},
    {"name": "Metacarpal", "region": "Hand", "type": "Long"},
    {"name": "Proximal Phalanx", "region": "Fingers", "type": "Long"},
    {"name": "Middle Phalanx", "region": "Fingers", "type": "Long"},
    {"name": "Distal Phalanx", "region": "Fingers", "type": "Long"},

    # Lower Extremities
    {"name": "Hip Bone", "region": "Pelvic Girdle", "type": "Irregular"},
    {"name": "Femur", "region": "Thigh", "type": "Long"},
    {"name": "Patella", "region": "Knee", "type": "Sesamoid"},
    {"name": "Tibia", "region": "Lower Leg", "type": "Long"},
    {"name": "Fibula", "region": "Lower Leg", "type": "Long"},
    {"name": "Calcaneus", "region": "Foot", "type": "Short"},
    {"name": "Talus", "region": "Foot", "type": "Short"},
    {"name": "Navicular", "region": "Foot", "type": "Short"},
    {"name": "Medial Cuneiform", "region": "Foot", "type": "Short"},
    {"name": "Intermediate Cuneiform", "region": "Foot", "type": "Short"},
    {"name": "Lateral Cuneiform", "region": "Foot", "type": "Short"},
    {"name": "Cuboid", "region": "Foot", "type": "Short"},
    {"name": "Metatarsal", "region": "Foot", "type": "Long"},
    {"name": "Proximal Phalanx", "region": "Toes", "type": "Long"},
    {"name": "Middle Phalanx", "region": "Toes", "type": "Long"},
    {"name": "Distal Phalanx", "region": "Toes", "type": "Long"}
]

muscles = [
    # Chest (Pectoral Region)
    {"name": "Pectoralis Major", "region": "Chest", "type": "Skeletal"},
    {"name": "Pectoralis Minor", "region": "Chest", "type": "Skeletal"},
    {"name": "Serratus Anterior", "region": "Chest", "type": "Skeletal"},
    {"name": "Subclavius", "region": "Chest", "type": "Skeletal"},

    # Back (Superficial)
    {"name": "Trapezius", "region": "Back", "type": "Skeletal"},
    {"name": "Latissimus Dorsi", "region": "Back", "type": "Skeletal"},
    {"name": "Levator Scapulae", "region": "Back", "type": "Skeletal"},
    {"name": "Rhomboid Major", "region": "Back", "type": "Skeletal"},
    {"name": "Rhomboid Minor", "region": "Back", "type": "Skeletal"},

    # Back (Deep)
    {"name": "Iliocostalis", "region": "Back", "type": "Skeletal"},
    {"name": "Longissimus", "region": "Back", "type": "Skeletal"},
    {"name": "Spinalis", "region": "Back", "type": "Skeletal"},
    {"name": "Semispinalis", "region": "Back", "type": "Skeletal"},
    {"name": "Multifidus", "region": "Back", "type": "Skeletal"},
    {"name": "Rotatores", "region": "Back", "type": "Skeletal"},
    {"name": "Splenius Capitis", "region": "Back", "type": "Skeletal"},
    {"name": "Splenius Cervicis", "region": "Back", "type": "Skeletal"},
    {"name": "Interspinales", "region": "Back", "type": "Skeletal"},
    {"name": "Intertransversarii", "region": "Back", "type": "Skeletal"},

    # Neck (Superficial)
    {"name": "Platysma", "region": "Neck", "type": "Skeletal"},
    {"name": "Sternocleidomastoid", "region": "Neck", "type": "Skeletal"},

    # Neck (Suprahyoid)
    {"name": "Digastric", "region": "Neck", "type": "Skeletal"},
    {"name": "Stylohyoid", "region": "Neck", "type": "Skeletal"},
    {"name": "Mylohyoid", "region": "Neck", "type": "Skeletal"},
    {"name": "Geniohyoid", "region": "Neck", "type": "Skeletal"},

    # Neck (Infrahyoid)
    {"name": "Sternohyoid", "region": "Neck", "type": "Skeletal"},
    {"name": "Omohyoid", "region": "Neck", "type": "Skeletal"},
    {"name": "Thyrohyoid", "region": "Neck", "type": "Skeletal"},
    {"name": "Sternothyroid", "region": "Neck", "type": "Skeletal"},

    # Neck (Deep)
    {"name": "Longus Capitis", "region": "Neck", "type": "Skeletal"},
    {"name": "Longus Colli", "region": "Neck", "type": "Skeletal"},
    {"name": "Scalenes", "region": "Neck", "type": "Skeletal"},

    # Shoulder
    {"name": "Deltoid", "region": "Shoulder", "type": "Skeletal"},
    {"name": "Supraspinatus", "region": "Shoulder", "type": "Skeletal"},
    {"name": "Infraspinatus", "region": "Shoulder", "type": "Skeletal"},
    {"name": "Teres Minor", "region": "Shoulder", "type": "Skeletal"},
    {"name": "Teres Major", "region": "Shoulder", "type": "Skeletal"},
    {"name": "Subscapularis", "region": "Shoulder", "type": "Skeletal"},

    # Arm
    {"name": "Biceps Brachii", "region": "Arm", "type": "Skeletal"},
    {"name": "Brachialis", "region": "Arm", "type": "Skeletal"},
    {"name": "Coracobrachialis", "region": "Arm", "type": "Skeletal"},
    {"name": "Triceps Brachii", "region": "Arm", "type": "Skeletal"},
    {"name": "Anconeus", "region": "Arm", "type": "Skeletal"},

    # Forearm (Anterior Compartment)
    {"name": "Pronator Teres", "region": "Forearm", "type": "Skeletal"},
    {"name": "Flexor Carpi Radialis", "region": "Forearm", "type": "Skeletal"},
    {"name": "Palmaris Longus", "region": "Forearm", "type": "Skeletal"},
    {"name": "Flexor Carpi Ulnaris", "region": "Forearm", "type": "Skeletal"},
    {"name": "Flexor Digitorum Superficialis", "region": "Forearm", "type": "Skeletal"},
    {"name": "Flexor Digitorum Profundus", "region": "Forearm", "type": "Skeletal"},
    {"name": "Flexor Pollicis Longus", "region": "Forearm", "type": "Skeletal"},
    {"name": "Pronator Quadratus", "region": "Forearm", "type": "Skeletal"},

    # Forearm (Posterior Compartment)
    {"name": "Brachioradialis", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Carpi Radialis Longus", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Carpi Radialis Brevis", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Digitorum", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Digiti Minimi", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Carpi Ulnaris", "region": "Forearm", "type": "Skeletal"},
    {"name": "Supinator", "region": "Forearm", "type": "Skeletal"},
    {"name": "Abductor Pollicis Longus", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Pollicis Brevis", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Pollicis Longus", "region": "Forearm", "type": "Skeletal"},
    {"name": "Extensor Indicis", "region": "Forearm", "type": "Skeletal"},

    # Hand
    {"name": "Abductor Pollicis Brevis", "region": "Hand", "type": "Skeletal"},
    {"name": "Flexor Pollicis Brevis", "region": "Hand", "type": "Skeletal"},
    {"name": "Opponens Pollicis", "region": "Hand", "type": "Skeletal"},
    {"name": "Adductor Pollicis", "region": "Hand", "type": "Skeletal"},
    {"name": "Abductor Digiti Minimi", "region": "Hand", "type": "Skeletal"},
    {"name": "Flexor Digiti Minimi Brevis", "region": "Hand", "type": "Skeletal"},
    {"name": "Opponens Digiti Minimi", "region": "Hand", "type": "Skeletal"},
    {"name": "Lumbricals", "region": "Hand", "type": "Skeletal"},
    {"name": "Palmar Interossei", "region": "Hand", "type": "Skeletal"},
    {"name": "Dorsal Interossei", "region": "Hand", "type": "Skeletal"},

    # Abdomen
    {"name": "Rectus Abdominis", "region": "Abdomen", "type": "Skeletal"},
    {"name": "External Oblique", "region": "Abdomen", "type": "Skeletal"},
    {"name": "Internal Oblique", "region": "Abdomen", "type": "Skeletal"},
    {"name": "Transversus Abdominis", "region": "Abdomen", "type": "Skeletal"}, 

    # Hip Muscles
    {"name": "Gluteus Maximus", "region": "Hip", "type": "Skeletal"},
    {"name": "Gluteus Medius", "region": "Hip", "type": "Skeletal"},
    {"name": "Gluteus Minimus", "region": "Hip", "type": "Skeletal"},
    {"name": "Iliacus", "region": "Hip", "type": "Skeletal"},
    {"name": "Psoas Major", "region": "Hip", "type": "Skeletal"},
    {"name": "Piriformis", "region": "Hip", "type": "Skeletal"},

    # Thigh (Quadriceps)
    {"name": "Rectus Femoris", "region": "Thigh (Anterior)", "type": "Skeletal"},
    {"name": "Vastus Lateralis", "region": "Thigh (Anterior)", "type": "Skeletal"},
    {"name": "Vastus Medialis", "region": "Thigh (Anterior)", "type": "Skeletal"},
    {"name": "Vastus Intermedius", "region": "Thigh (Anterior)", "type": "Skeletal"},

    # Thigh (Hamstrings)
    {"name": "Biceps Femoris", "region": "Thigh (Posterior)", "type": "Skeletal"},
    {"name": "Semitendinosus", "region": "Thigh (Posterior)", "type": "Skeletal"},
    {"name": "Semimembranosus", "region": "Thigh (Posterior)", "type": "Skeletal"},

    # Inner Thigh (Adductors)
    {"name": "Adductor Longus", "region": "Thigh (Medial)", "type": "Skeletal"},
    {"name": "Adductor Brevis", "region": "Thigh (Medial)", "type": "Skeletal"},
    {"name": "Adductor Magnus", "region": "Thigh (Medial)", "type": "Skeletal"},
    {"name": "Gracilis", "region": "Thigh (Medial)", "type": "Skeletal"},
    {"name": "Pectineus", "region": "Thigh (Medial)", "type": "Skeletal"},

    # Lower Leg (Calf Muscles)
    {"name": "Gastrocnemius", "region": "Calf", "type": "Skeletal"},
    {"name": "Soleus", "region": "Calf", "type": "Skeletal"},
    {"name": "Plantaris", "region": "Calf", "type": "Skeletal"},

    # Lower Leg (Anterior Muscles)
    {"name": "Tibialis Anterior", "region": "Lower Leg (Anterior)", "type": "Skeletal"},
    {"name": "Extensor Digitorum Longus", "region": "Lower Leg (Anterior)", "type": "Skeletal"},
    {"name": "Extensor Hallucis Longus", "region": "Lower Leg (Anterior)", "type": "Skeletal"},

    # Lower Leg (Lateral Muscles)
    {"name": "Fibularis Longus (Peroneus Longus)", "region": "Lower Leg (Lateral)", "type": "Skeletal"},
    {"name": "Fibularis Brevis (Peroneus Brevis)", "region": "Lower Leg (Lateral)", "type": "Skeletal"}
]

# CSS for background and content styling
background_url = "https://img.pikbest.com/backgrounds/20191127/skeleton-hand-seamless-pattern-on-black-background--halloween-bones-pattern-background--v_1605390jpg!bw700"
custom_css = f"""
<style>
    body {{
        background-image: url("{background_url}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .main-container {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }}
    .stButton > button {{
        background-color: #ff5722;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }}
    .stButton > button:hover {{
        background-color: #e64a19;
    }}
    .stTextInput > div > div > input {{
        border: 1px solid #ff5722;
        color: white;
        background-color: black;
        border-radius: 5px;
        padding: 5px;
    }}
</style>
"""

# Apply the CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Function to get a random entity
def get_random_entity(entities):
    return random.choice(entities)

# Function to mask the word with underscores
def mask_word(word, revealed_indices=[]):
    return " ".join([char if idx in revealed_indices else "_" for idx, char in enumerate(word)])

# Function to check similarity between two words
def is_guess_correct(guess, target, threshold=0.85):
    # Normalize both strings: lowercase and strip spaces
    guess = guess.lower().strip()
    target = target.lower().strip()
    # Calculate similarity using SequenceMatcher
    similarity = SequenceMatcher(None, guess, target).ratio()
    return similarity >= threshold

# Combine bones and muscles into a single list
# Combine bones and muscles into a single list with an explicit category
entities = [
    *[{"name": e["name"], "region": e["region"], "type": e["type"], "category": "Bone"} for e in bones],
    *[{"name": e["name"], "region": e["region"], "type": e["type"], "category": "Muscle"} for e in muscles],
]

# Initialize session state
if "entity" not in st.session_state:
    st.session_state["entity"] = get_random_entity(entities)
if "guesses" not in st.session_state:
    st.session_state["guesses"] = []
if "hints" not in st.session_state:
    st.session_state["hints"] = 0
if "lives" not in st.session_state:
    st.session_state["lives"] = 6
if "revealed_hints" not in st.session_state:
    st.session_state["revealed_hints"] = []

# Get the current entity
hidden_word = st.session_state["entity"]["name"].lower()
masked_word = mask_word(hidden_word)

# Streamlit interface
st.title("Bone and Muscle Wordle")
st.write(f"Guess the entity: {masked_word} ({len(hidden_word)} letters)")

# Define all hints
all_hints = [
    f"Category: {st.session_state['entity']['category']}",
    f"Region: {st.session_state['entity']['region']}",
    f"Type: {st.session_state['entity']['type']}",
]

# Show revealed hints so far
if st.session_state["revealed_hints"]:
    st.write("Hints revealed so far:")
    for hint in st.session_state["revealed_hints"]:
        st.write(f"- {hint}")

# Provide the next hint when the button is clicked
if st.session_state["hints"] < len(all_hints):
    if st.button(f"Reveal Hint {st.session_state['hints'] + 1}"):
        next_hint = all_hints[st.session_state["hints"]]
        st.session_state["revealed_hints"].append(next_hint)
        st.write(f"Hint: {next_hint}")
        st.session_state["hints"] += 1
        st.session_state["lives"] -= 1

# Input for guesses
guess = st.text_input("Your guess:").strip()
if st.button("Submit Guess"):
    if guess:
        if is_guess_correct(guess, hidden_word):
            st.success(f"Correct! The entity is {st.session_state['entity']['name']}!")
            # Reset game state
            st.session_state["entity"] = get_random_entity(entities)
            st.session_state["guesses"] = []
            st.session_state["hints"] = 0
            st.session_state["lives"] = 6
            st.session_state["revealed_hints"] = []
        else:
            st.session_state["guesses"].append(guess)
            st.session_state["lives"] -= 1
            if st.session_state["lives"] == 0:
                st.error(f"Out of guesses! The correct answer was {st.session_state['entity']['name']}.")
                # Reset game state
                st.session_state["entity"] = get_random_entity(entities)
                st.session_state["guesses"] = []
                st.session_state["hints"] = 0
                st.session_state["lives"] = 6
                st.session_state["revealed_hints"] = []
            else:
                st.warning(f"Incorrect! {st.session_state['lives']} guesses left.")

# Display previous guesses
if st.session_state["guesses"]:
    st.write("Your guesses so far:")
    for g in st.session_state["guesses"]:
        st.write(f"- {g}")

# Display remaining lives
st.write(f"Lives remaining: {st.session_state['lives']}")

# cd "/Users/arjunghumman/Downloads/VS Code Stuff/Python/ANATOMY WORDLE"
# streamlit run anatomy.py