import streamlit as st
import sys
from pathlib import Path
from PIL import Image
import io
import random
from datetime import datetime

# Add parent directory to path
#sys.path.append(str(Path(__file__).parent.parent))

from storage import StorageManager

# Page configuration
#st.set_page_config(
#    page_title="VQA - Smart Vision",
#    page_icon="🖼️",
#    layout="wide"
#)

# Load CSS
def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d1b3d 50%, #1a1a2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d1b3d 100%);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-header {
        text-align: center;
        color: #b8b8d0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 2rem;
    }
    
    .output-section {
        background: rgba(102, 126, 234, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .story-section {
        background: rgba(118, 75, 162, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #764ba2;
        margin: 1rem 0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize storage manager
storage_manager = StorageManager()

# Check authentication
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to access this page")
    st.stop()

# Placeholder VQA function
def answer_question(image, question):
    """
    Placeholder function for VQA model
    Replace with actual model inference later
    """
    # Simulate processing delay
    import time
    time.sleep(1)
    
    # Generate placeholder answer based on question keywords
    question_lower = question.lower()
    
    if 'color' in question_lower or 'colour' in question_lower:
        answers = ["The dominant color appears to be blue", "I can see red and yellow tones", "The image has warm brown colors"]
        confidence = random.uniform(0.75, 0.95)
    elif 'how many' in question_lower or 'count' in question_lower:
        answers = ["I count approximately 3 objects", "There are 2 main elements", "I see 5 distinct items"]
        confidence = random.uniform(0.70, 0.90)
    elif 'what' in question_lower:
        answers = ["This appears to be a scene with natural elements", "I can see outdoor scenery", "This looks like an object or landscape"]
        confidence = random.uniform(0.65, 0.85)
    elif 'where' in question_lower:
        answers = ["This appears to be outdoors", "The setting looks like an indoor space", "This could be in a natural environment"]
        confidence = random.uniform(0.60, 0.80)
    else:
        answers = ["Based on the visual content, this is likely the case", "The image suggests this interpretation", "From what I can observe, this seems accurate"]
        confidence = random.uniform(0.70, 0.88)
    
    answer = random.choice(answers)
    return answer, round(confidence, 3)

# Placeholder story generation function
def generate_story(image, style):
    """
    Placeholder function for story generation
    Replace with actual AI model later
    """
    import time
    time.sleep(1.5)
    
    stories = {
        "Funny": [
            "Once upon a time, in a world where everything was slightly askew, this scene unfolded with hilarious consequences. The objects in the image seemed to have a mind of their own, creating chaos and laughter wherever they went. Little did anyone know, this was just the beginning of an absurdly entertaining adventure.",
            "In the great comedy of life, this moment captured the essence of unexpected humor. The elements in this image were having the time of their lives, completely unaware of how ridiculous they looked to observers. And that, dear friends, is what made it absolutely perfect.",
        ],
        "Emotional": [
            "This image tells a story of moments frozen in time, carrying with it the weight of memories and emotions. Each element speaks to something deeper, a connection to experiences that transcend the visual and touch the heart. It reminds us of the beauty found in everyday moments.",
            "There is something profoundly moving about this scene. It captures a fleeting moment that carries echoes of nostalgia, hope, and the bittersweet nature of life's journey. Looking at it, one cannot help but reflect on the precious, ephemeral nature of our experiences.",
        ],
        "Professional": [
            "This image represents a carefully composed visual narrative that demonstrates key principles of composition and aesthetic design. The arrangement of elements creates a balanced framework that effectively communicates its intended message. From a technical perspective, the lighting and spatial relationships contribute to its overall impact.",
            "Analysis of this visual content reveals a structured approach to image composition. The positioning of elements follows established design principles, creating visual hierarchy and focal points that guide viewer attention. This demonstrates professional application of photographic and compositional techniques.",
        ],
        "Creative": [
            "Imagine this scene as a gateway to another dimension, where reality bends and transforms. The elements within paint a surreal landscape of possibility, inviting us to question what we see and reimagine it through the lens of pure imagination. This is not just an image, but a portal to infinite stories waiting to be told.",
            "In the canvas of dreams, this moment exists as a crystallized fragment of infinite possibilities. Each component dances in harmony with abstract concepts and tangible realities, weaving together a tapestry that defies conventional narrative. It is art, it is mystery, it is everything and nothing all at once.",
        ]
    }
    
    return random.choice(stories[style])

# Main page
def main():
    st.markdown('<h1 class="main-header">Visual Question Answering</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload an image and ask questions or generate stories</p>', unsafe_allow_html=True)
    
    # Create two-column layout
    col_input, col_output = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Input Section")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Upload an image to analyze"
        )
        
        if uploaded_file:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=400)
            
            # Store image name
            image_name = uploaded_file.name
            
            st.markdown("---")
            
            # Question input
            st.markdown("### Ask a Question")
            question = st.text_area(
                "Enter your question about the image",
                height=100,
                placeholder="e.g., What colors are in this image? How many objects are there?"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                ask_button = st.button("Get Answer", use_container_width=True)
            
            # Story generation
            st.markdown("---")
            st.markdown("### Generate Story")
            
            story_style = st.selectbox(
                "Select story style",
                ["Funny", "Emotional", "Professional", "Creative"]
            )
            
            with col_btn2:
                story_button = st.button("Generate Story", use_container_width=True)
            
            # Process VQA
            if ask_button and question:
                with st.spinner("Processing your question..."):
                    answer, confidence = answer_question(image, question)
                    
                    # Store in session state
                    st.session_state.vqa_result = {
                        'image': image,
                        'image_name': image_name,
                        'question': question,
                        'answer': answer,
                        'confidence': confidence
                    }
                    
                    # Save to history
                    storage_manager.add_interaction(
                        username=st.session_state.username,
                        image_name=image_name,
                        question=question,
                        answer=answer,
                        confidence=confidence
                    )
                    
                    st.rerun()
            
            elif ask_button:
                st.error("Please enter a question")
            
            # Process story generation
            if story_button:
                with st.spinner(f"Generating {story_style.lower()} story..."):
                    story = generate_story(image, story_style)
                    
                    # Store in session state
                    st.session_state.story_result = {
                        'story': story,
                        'style': story_style,
                        'image_name': image_name
                    }
                    
                    # Update history with story
                    storage_manager.add_interaction(
                        username=st.session_state.username,
                        image_name=image_name,
                        question="Story Generation",
                        answer="Story generated",
                        confidence=1.0,
                        story=story,
                        story_style=story_style
                    )
                    
                    st.rerun()
        
        else:
            st.info("Upload an image to get started")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_output:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Results")
        
        # Display VQA results
        if hasattr(st.session_state, 'vqa_result') and st.session_state.vqa_result:
            result = st.session_state.vqa_result
            
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.markdown("#### Question & Answer")
            
            st.markdown(f"**Question:** {result['question']}")
            st.markdown(f"**Answer:** {result['answer']}")
            
            # Display confidence
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                st.metric("Confidence Score", f"{result['confidence']:.1%}")
            
            # Confidence indicator
            confidence_color = "green" if result['confidence'] > 0.8 else "orange" if result['confidence'] > 0.6 else "red"
            st.progress(result['confidence'])
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display story results
        if hasattr(st.session_state, 'story_result') and st.session_state.story_result:
            story_data = st.session_state.story_result
            
            st.markdown('<div class="story-section">', unsafe_allow_html=True)
            st.markdown(f"#### Generated Story ({story_data['style']})")
            
            st.markdown(story_data['story'])
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if not hasattr(st.session_state, 'vqa_result') and not hasattr(st.session_state, 'story_result'):
            st.info("Upload an image and ask a question or generate a story to see results here")
        
        st.markdown('</div>', unsafe_allow_html=True)

#if __name__ == "__main__":
#   main()
