import streamlit as st
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from PIL import Image
import matplotlib.pyplot as plt

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Convert PDF content to Text format
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

# Function to create a doughnut chart
def create_doughnut_chart(percentage):
    fig, ax = plt.subplots(figsize=(6, 6))
    sizes = [percentage, 100 - percentage]
    colors = ['#4CAF50', '#E0E0E0']
    explode = (0.1, 0)  
    ax.pie(sizes, colors=colors, startangle=90, explode=explode, wedgeprops=dict(width=0.3))
    ax.text(0, 0, f'{percentage}%', ha='center', va='center', fontsize=24, fontweight='bold')
    ax.set_title("Match Percentage", fontsize=16)
    ax.axis('equal')  
    return fig

# Streamlit UI
st.set_page_config(page_title="Resume ATS Tracker", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    .stApp {
        background-color:#ADD8E6;
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: black;
        font-family: 'Roboto', sans-serif;
        margin:20px;
    }
    p, div, span {
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    .stImage {
        margin: auto;
        display: block;
        margin: 12px 12px;
        border-radius: 15px;
        
    }
    img[src="https://carrercraftresumeanalyzerproject.streamlit.app:443/~/+/media/33fd7a949eea48174eef7209b4f9b6445c7e2cc5c694ea7a6f14b5e7.jpg"]{
        position:absolute;
        left:25px;
        top:40px;
        width:100px;
    }
    img[style="width: 287.203px;"]{
        position:absolute;
        left:-20px;
    }
    img[src="https://carrercraftresumeanalyzerproject.streamlit.app:443/~/+/media/c2d373f3e6c34e1aec9ad8b4e52d5cc229c52ca03f6b7c65cbe4b8d2.jpg"]{
        position:absolute;
        right:-50px;
        width:100px;
        height:500px;
        margin-top:0px auto;
        
    }
    img[src="http://localhost:8501/media/21535ea99dc1fb6e337e6bbb7f629a85cb9cad70cf96ca8e8032fa7f.jpg"]{
        position:absolute;
        left:-30px;
        margin-top:60px;
    }
    div[style*="width:188.812px"]{
        font-size:1rem;
        font-weight:bold;
        
    }
    .st-emotion-cache-1b0udgb.e115fcil0{
        font-size:1.5rem;
        font-weight:900;
        color:black;
        transform:translateX(30px);
        transform.translateY(60px);
        margin-top:0px auto;
        position:absolute;
        bottom:-550px;
        right:-25px;
        
    }
    #navigate-the-job-market-with-confidence{
        margin-left:-5px;
    }
    div[data-testid="stImageContainer"]{
        margin-left:-30px;
    }
    video[ autoplay="loop="]{
        position:absolute;
        left:-30px;
        
    
    }

    .stButton>button {
        background-color:orange;
        color: #ffffff ;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #004d00;
    }
    .header-title {
        text-align: center;
        font-weight: 700;
        font-size: 2.5em;
    }
    .sub-header {
        text-align: center;
        font-weight:900;
        font-size: 1.5em;
        margin-left:650px;
        position:relative;
        margin-top:-50px;

    }
    .description {
        text-align: justify;
        font-weight: 300;
        font-size: 1.2rem;
    }
    .offerings {
        font-weight: 300;
        font-size: 1.2em;
        margin:20px;
    }
    .faq-container {
        background-color: white;
        border-radius: 0px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-left:650px;
        position:relative;
        margin-top:40px;
        border-bottom-right-radius:15%;
        box-shadow:0px 0px 8px navy;
    }
    .faq-question {
        font-weight: 400;
        font-size: 1.2em;
        margin-bottom:10px;
        position:relative;
     
    }
    .faq-answer {
        font-weight: 300;
        font-size: 1.2em;
        margin-bottom: 30px;
       
    }
    .stTextInput > div, .stTextArea > div {
        background-color: #d4edda;  /* Light green background */
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

avs.add_vertical_space(4)
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<h1 style='text-align: center; color:navy;'>CareerCraft</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style ='margin-left:-6px;'>Perfect Your Fit with Precision</h2>",unsafe_allow_html=True)
    st.markdown(""" 
                <p class='description'>
                Imagine a tool that not only evaluates the effectiveness of a resume but also guides job seekers in crafting an exceptional one. Our ATS-optimized Resume Analyzer leverages AI to analyze resumes, offering a precise score based on alignment with ATS (Applicant Tracking System) standards and hiring preferences. By providing actionable insights and improvement suggestions, this analyzer helps applicants refine their resumes for maximum impact, ensuring they stand out and successfully pass through hiring filters with ease.
                </p>
                """, unsafe_allow_html=True)
with col2:
     img1 = Image.open("./Images/Image1.jpg")
     st.image(img1, use_column_width=True)

avs.add_vertical_space(10)

col1, col2 = st.columns([3, 2])
with col2:
    st.header("Broad Range of Offerings")
    st.markdown(""" 
                <ul class='offerings'>
                    <li><a href ="https://g.co/gemini/share/4c8f16820916">ATS-Optimized Resume Analysis</a></li>
                    <li><a href ="https://g.co/gemini/share/3fd8a30ec1cb">Resume Optimization</a></li>
                    <li><a href ="https://g.co/gemini/share/8dfda91fb2ea">Skill Enhancement</a></li>
                    <li><a href ="https://g.co/gemini/share/e07941e79992">Career Progression Guidance</a></li>
                    <li><a href ="https://g.co/gemini/share/f4a561f67e89">Tailored Profile Summaries</a></li>
                    <li><a href ="https://g.co/gemini/share/294cf52f9774">Streamlined Application Process</a></li>
                    <li><a href ="">Personalized Recommendations</a></li>
                    <li><a href ="https://g.co/gemini/share/ffb2fc0ae5fb">Efficient Career Navigation</a></li>
                </ul>
                """, unsafe_allow_html=True)
with col1:
   img2 = Image.open("./Images/Image2.jpg")
   st.image(img2, use_column_width=True, caption="Optimize Your Resume")

avs.add_vertical_space(10)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<h1 class='header-title'>Navigate Your Carrer Journey</h1>", unsafe_allow_html=True)
    jd = st.text_area("Enter the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")
    submit = st.button("Submit")
    if submit:
        if uploaded_file is not None and jd:
            text = input_pdf_text(uploaded_file)
            input_prompt = f"""
            As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions. In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement. Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords with utmost accuracy.
            resume: {text}
            description: {jd}
            I want the response in the following structure:
            The first line indicates the percentage match with the job description (JD).
            The second line presents a list of missing keywords.
            The third section provides a profile summary.
            Mention the title for all the three sections.
            While generating the response put some space to separate all the three sections.
            """
            response = get_gemini_response(input_prompt)
            if response:
                st.subheader("Analysis Result")
                left_col, right_col = st.columns([2, 1])
                with left_col:
                    st.markdown(response)
                match_percentage = 0 
                try:
                    match_percentage = int(response.split('\n')[0].split(' ')[-1].strip('%'))
                except:
                    st.error("Failed to extract match percentage from the response.")
            
                with right_col:
                    fig = create_doughnut_chart(match_percentage)
                    st.pyplot(fig)
        else:
            st.error("Please provide both the job description and upload your resume.")
with col2:
    img3 = Image.open("./Images/Image3.jpg")
    st.image(img3, use_column_width=True, caption="Career Guidance")

avs.add_vertical_space(10)

col1, col2 = st.columns([2, 3])
with col2:
    import base64

# Load video file and encode it to base64
video_path = "./Images/AdvanceAnalysisAIVideo.mp4"
with open(video_path, "rb") as video_file:
    video_base64 = base64.b64encode(video_file.read()).decode("utf-8")

# Embed the video in HTML without a playbar
video_html = f"""
    <video autoplay loop muted style="width: 40%; border-radius: 15px;">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <p style="text-align:center;font-weight:900;margin-right:750px;font-size:1.5rem; ">Advance Analysis</p>
"""

# Display the video in Streamlit
st.components.v1.html(video_html, height=500)
st.markdown("<h1 class='sub-header'>FAQs</h1>", unsafe_allow_html=True)
st.markdown(""" 
                <div class="faq-container">
                    <p style= class='faq-question'>Question: How does CareerCraft analyze resumes and job descriptions? </p>
                    <p class='faq-answer'>Answer: CareerCraft uses advanced algorithms to analyze resumes and job descriptions, identifying key keywords and assessing compatibility between the two.</p>
                </div>
                <div class="faq-container">
                    <p class='faq-question'>Question: Is CareerCraft suitable for both entry-level and experienced professionals?</p>
                    <p class='faq-answer'>Answer: Absolutely! CareerCraft caters to job seekers at all career stages, offering tailored insights and guidance to enhance their resumes and advance their careers.</p>
                </div>
                <div class="faq-container">
                    <p class='faq-question'>Question: Can CareerCraft suggest improvements for my resume?</p>
                    <p class='faq-answer'>Answer: Yes, CareerCraft provides personalized recommendations to optimize your resume for specific job openings, including suggestions for missing keywords and alignment with desired job roles.</p>
                </div>
                """, unsafe_allow_html=True)



avs.add_vertical_space(10)
