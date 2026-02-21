import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import textwrap
import random

# -------- Load HuggingFace Model --------
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")

generator = load_model()

# -------- Template Lists --------
meme_templates = [
    "templates/meme1.jpg",
    "templates/meme2.jpg",
    "templates/meme3.jpg",
    "templates/meme4.jpg",
    "templates/meme5.jpg",
    "templates/meme6.jpg"
]

poster_templates = [
    "templates/poster1.jpg",
    "templates/poster2.jpg",
    "templates/poster3.jpg",
    "templates/poster4.jpg"
]

all_templates = meme_templates + poster_templates

# -------- AI Caption Generation --------
def generate_caption(topic):
    prompt = f"Create a short funny caption about {topic}."
    result = generator(prompt, max_length=40, num_return_sequences=1)
    text = result[0]['generated_text']
    caption = text.replace(prompt, "").strip()
    return caption

# -------- Smart Template Selection --------
def choose_template(topic, mode):
    topic = topic.lower()

    if mode == "Random":
        return random.choice(all_templates)

    elif mode == "Auto (Smart Selection)":
        if any(word in topic for word in ["fest", "event", "celebration", "conference"]):
            return random.choice(poster_templates)
        elif any(word in topic for word in ["funny", "joke", "meme", "laugh"]):
            return random.choice(meme_templates)
        else:
            return random.choice(all_templates)

    elif mode == "Manual - Meme Only":
        return random.choice(meme_templates)

    elif mode == "Manual - Poster Only":
        return random.choice(poster_templates)

# -------- Add Text To Image --------
def create_image(template_path, caption):
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    width, height = img.size
    wrapped_text = textwrap.fill(caption, width=30)

    font = ImageFont.load_default()

    draw.text(
        (width/2, height - 80),
        wrapped_text,
        fill="white",
        anchor="mm",
        font=font
    )

    return img

# -------- Streamlit UI --------
st.title("🎨 AI Meme & Poster Creator")
st.write("Smart AI-based meme and poster generator")

topic = st.text_input("Enter Topic:")

mode = st.selectbox(
    "Select Generation Mode:",
    [
        "Auto (Smart Selection)",
        "Random",
        "Manual - Meme Only",
        "Manual - Poster Only"
    ]
)

if st.button("Generate"):
    if topic:
        with st.spinner("Generating AI Caption..."):
            caption = generate_caption(topic)

        template_choice = choose_template(topic, mode)

        st.success("Caption Generated!")
        st.write("👉", caption)

        generated_image = create_image(template_choice, caption)
        st.image(generated_image)

        generated_image.save("output_generated.png")

        with open("output_generated.png", "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name="AI_Generated_Image.png",
                mime="image/png"
            )
    else:
        st.warning("Please enter a topic.")