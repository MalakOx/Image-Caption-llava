import streamlit as st
import requests
import time
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Image Caption Generator - LLaVA",
    page_icon="🖼️",
    layout="wide"
)

# Main title
st.title("🖼️ Image Caption Generator with LLaVA")
st.write("Upload an image and let LLaVA AI generate detailed captions!")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ Information")
    st.write("**Model:** LLaVA via Ollama")
    st.write("**Backend:** FastAPI")
    st.write("**Frontend:** Streamlit")
    st.write("**Capabilities:** Vision + Language")
    
    # API connection test
    st.header("🔗 Connection Status")
    if st.button("Test Connection"):
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ API Connected")
                st.success(f"✅ Ollama: {data.get('ollama', 'unknown')}")
                if data.get('llava_available'):
                    st.success("✅ LLaVA Model Available")
                else:
                    st.warning("⚠️ LLaVA Model Not Found")
                
                with st.expander("Available Models"):
                    models = data.get('available_models', [])
                    for model in models:
                        st.write(f"• {model}")
            else:
                st.error("❌ API Not Accessible")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.header("📝 Supported Formats")
    st.write("• PNG")
    st.write("• JPG/JPEG")
    st.write("• WebP")
    st.write("• GIF")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png", "jpg", "jpeg", "webp", "gif"],
        help="Upload an image to generate a caption"
    )
    
    # Display uploaded image
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image info
            with st.expander("📊 Image Information"):
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**Size:** {image.size}")
                st.write(f"**Format:** {image.format}")
                st.write(f"**Mode:** {image.mode}")
                st.write(f"**File Size:** {len(uploaded_file.getvalue())} bytes")
        
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
    
    # Custom prompt option
    st.header("🎯 Caption Options")
    use_custom_prompt = st.checkbox("Use Custom Prompt")
    
    if use_custom_prompt:
        custom_prompt = st.text_area(
            "Enter your custom prompt:",
            value="Describe this image in detail",
            height=100,
            help="Customize how you want the image to be described"
        )
    
    # Predefined prompts
    st.subheader("💡 Quick Prompts")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        if st.button("🏞️ Detailed Description"):
            if not use_custom_prompt:
                st.session_state.selected_prompt = "Provide a detailed description of this image, including objects, people, setting, colors, and atmosphere."
        
        if st.button("🎨 Artistic Style"):
            if not use_custom_prompt:
                st.session_state.selected_prompt = "Describe the artistic style, composition, and visual elements of this image."
    
    with col_p2:
        if st.button("👥 People & Actions"):
            if not use_custom_prompt:
                st.session_state.selected_prompt = "Focus on describing the people in this image and what they are doing."
        
        if st.button("🌍 Scene & Context"):
            if not use_custom_prompt:
                st.session_state.selected_prompt = "Describe the scene, location, and context of this image."

with col2:
    st.header("🎯 Generated Caption")
    
    if uploaded_file is not None:
        # Determine which prompt to use
        if use_custom_prompt:
            prompt_to_use = custom_prompt
            endpoint = "/caption/custom/"
        elif hasattr(st.session_state, 'selected_prompt'):
            prompt_to_use = st.session_state.selected_prompt
            endpoint = "/caption/custom/"
        else:
            prompt_to_use = None
            endpoint = "/caption/"
        
        if st.button("🔍 Generate Caption", type="primary", use_container_width=True):
            with st.spinner("Analyzing image... This may take a moment..."):
                try:
                    start_time = time.time()
                    
                    # Prepare the request
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    if endpoint == "/caption/custom/":
                        data = {"prompt": prompt_to_use}
                        response = requests.post(
                            f"http://localhost:8000{endpoint}",
                            files=files,
                            data=data,
                            timeout=90
                        )
                    else:
                        response = requests.post(
                            f"http://localhost:8000{endpoint}",
                            files=files,
                            timeout=90
                        )
                    
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        result = response.json()
                        caption = result.get("caption", "No caption generated")
                        
                        # Display result
                        st.success("✅ Caption Generated!")
                        st.write("### 📝 Caption:")
                        st.write(caption)
                        
                        # Additional info
                        st.write(f"⏱️ **Processing Time:** {end_time - start_time:.2f} seconds")
                        
                        # Show prompt used (if custom)
                        if "prompt" in result:
                            with st.expander("🎯 Prompt Used"):
                                st.code(result["prompt"])
                        
                        # File details
                        with st.expander("📄 File Details"):
                            st.write(f"**Filename:** {result.get('filename', 'Unknown')}")
                            st.write(f"**File Size:** {result.get('file_size', 0)} bytes")
                    
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                        if response.text:
                            st.code(response.text)
                
                except requests.exceptions.Timeout:
                    st.error("⏰ Timeout: Image analysis is taking too long. Try with a smaller image.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Connection Error: Make sure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"❌ Unexpected Error: {str(e)}")
    
    else:
        st.info("👆 Please upload an image to generate a caption")

# Clear selected prompt when not using custom
if not use_custom_prompt and hasattr(st.session_state, 'selected_prompt'):
    del st.session_state.selected_prompt

# Usage instructions
st.header("📖 How to Use")
st.write("""
1. **Upload an image** using the file uploader on the left
2. **Choose caption style** - use default or custom prompt
3. **Click 'Generate Caption'** to analyze the image
4. **View the generated caption** on the right side
5. **Try different prompts** for varied descriptions
""")

# Tips section
st.header("💡 Tips for Better Results")
col_tip1, col_tip2 = st.columns(2)

with col_tip1:
    st.write("""
    **Image Quality:**
    - Use clear, well-lit images
    - Avoid blurry or very dark images
    - Higher resolution generally works better
    """)

with col_tip2:
    st.write("""
    **Custom Prompts:**
    - Be specific about what you want described
    - Ask for particular details (colors, emotions, etc.)
    - Use clear, direct language
    """)

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ using LLaVA, FastAPI, and Streamlit*")