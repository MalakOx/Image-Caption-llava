# 🖼️ Image Caption Generator with LLaVA

An AI-powered application that uses the **LLaVA (Large Language and Vision Assistant)** model via Ollama to generate detailed captions for uploaded images.

## ✨ Features

- **Vision-Language Model** - LLaVA combines computer vision with natural language processing
- **FastAPI Backend** - High-performance, documented REST API
- **Streamlit Frontend** - Interactive and user-friendly interface
- **Custom Prompts** - Customize how you want images described
- **Multiple Image Formats** - Support for PNG, JPG, JPEG, WebP, and GIF
- **Real-time Processing** - Generate captions on-demand

## 🎯 Capabilities

The application can:
- **Generate detailed descriptions** of uploaded images
- **Identify objects, people, and scenes** in photographs
- **Describe artistic style and composition** of artwork
- **Analyze context and atmosphere** of images
- **Respond to custom prompts** for specific analysis needs

## 🛠️ Technologies Used

- **Python 3.8+**
- **LLaVA Model** - State-of-the-art vision-language model
- **Ollama** - Local AI model execution platform
- **FastAPI** - Modern web framework for building APIs
- **Streamlit** - Framework for creating interactive web applications
- **Pillow (PIL)** - Python Imaging Library for image processing

## 📋 Prerequisites

1. **Python 3.8 or newer**
2. **Ollama installed and configured**
3. **Git** (for cloning and version control)
4. **Sufficient RAM** (LLaVA requires more memory than text-only models)

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/image-caption-llava.git
cd image-caption-llava
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download LLaVA Model

```bash
ollama pull llava
```

**Note:** LLaVA is a larger model and may take some time to download.

### 5. Start FastAPI Backend

```bash
uvicorn backend.main:app --reload
```

The API will be accessible at: http://localhost:8000

### 6. Start Streamlit Frontend

In a new terminal:

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Streamlit
streamlit run frontend/app.py
```

The application will be accessible at: http://localhost:8501

## 📁 Project Structure

```
image-caption-llava/
│
├── backend/
│   └── main.py              # FastAPI backend with image processing
│
├── frontend/
│   └── app.py               # Streamlit interface
│
├── requirements.txt         # Python dependencies
├── README.md               # Documentation
└── .gitignore             # Git ignore file
```

## 🔧 API Endpoints

### POST `/caption/`
Generates a caption for an uploaded image using default prompt

**Parameters:**
- `file` (UploadFile): Image file to analyze

**Response:**
```json
{
  "filename": "example.jpg",
  "caption": "A detailed description of the image...",
  "file_size": 123456
}
```

### POST `/caption/custom/`
Generates a caption using a custom prompt

**Parameters:**
- `file` (UploadFile): Image file to analyze
- `prompt` (string): Custom prompt for image analysis

**Response:**
```json
{
  "filename": "example.jpg",
  "prompt": "Custom prompt used",
  "caption": "Response based on custom prompt...",
  "file_size": 123456
}
```

### GET `/health`
Checks API status and model availability

**Response:**
```json
{
  "status": "healthy",
  "ollama": "connected",
  "llava_available": true,
  "available_models": ["llava:latest", "mistral:latest"]
}
```

## 🎮 Usage

1. **Open the application** in your browser (http://localhost:8501)
2. **Upload an image** using the file uploader
3. **Choose caption style:**
   - Use default detailed description
   - Select a quick prompt option
   - Write a custom prompt
4. **Click 'Generate Caption'** to analyze the image
5. **View the generated caption** and additional details

## 🎯 Prompt Examples

### Detailed Description
*"Provide a detailed description of this image, including objects, people, setting, colors, and atmosphere."*

### Artistic Analysis  
*"Describe the artistic style, composition, and visual elements of this image."*

### People Focus
*"Focus on describing the people in this image and what they are doing."*

### Scene Context
*"Describe the scene, location, and context of this image."*

## 🐛 Troubleshooting

### Issue: "Error connecting to Ollama"
- Check that Ollama is running: `ollama serve`
- Verify LLaVA model is installed: `ollama list`

### Issue: "LLaVA Model Not Found"
- Pull the model: `ollama pull llava`
- Wait for download to complete (model is ~4GB)

### Issue: Slow processing
- LLaVA processing is computationally intensive
- First request may take longer (model loading)
- Consider using smaller images for faster processing

### Issue: Out of memory errors
- LLaVA requires significant RAM
- Close other applications to free memory
- Try smaller image files

## 🔄 Supported Image Formats

- **PNG** - Portable Network Graphics
- **JPG/JPEG** - Joint Photographic Experts Group
- **WebP** - Modern web image format
- **GIF** - Graphics Interchange Format

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. **Fork** the project
2. **Create a branch** for your feature
3. **Commit** your changes  
4. **Push** to the branch
5. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- **LLaVA Team** for the incredible vision-language model
- **Ollama** for making local AI model execution accessible
- **FastAPI** and **Streamlit** for excellent frameworks
- The open-source community for tools and libraries

## 🔮 Future Enhancements

- **Batch processing** for multiple images
- **Image comparison** and analysis
- **Export captions** to various formats
- **Advanced prompt templates**
- **Image editing suggestions**

---

*Built with ❤️ using LLaVA, FastAPI, and Streamlit*