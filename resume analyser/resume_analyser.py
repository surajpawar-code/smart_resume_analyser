import os
import streamlit as st
import nltk
import spacy
import pandas as pd
import base64
import random
import datetime
import pymysql
import io
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from PIL import Image
from streamlit_tags import st_tags
import plotly.express as px
import pafy
import bcrypt

# Load language models
nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')

# Constants
ACTIVITIES = ["Normal User", "Admin"]

# Connect to database
try:
    connection = pymysql.connect(host='localhost', user='root', password='1234', db='sra')
    cursor = connection.cursor()
except Exception as e:
    st.error(f"Database connection error: {e}")

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(stored_password, provided_password):
    """Check hashed password."""
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

def fetch_yt_video(link):
    """Fetch video title from YouTube link."""
    try:
        video = pafy.new(link)
        return video.title
    except Exception as e:
        st.error(f"Error fetching video: {e}")
        return None

def get_table_download_link(df, filename, text):
    """Generates a link allowing the data in a given pandas DataFrame to be downloaded as CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Convert to bytes
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

def pdf_reader(file):
    """Extract text from PDF file."""
    try:
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def show_pdf(file_path):
    """Display a PDF file in the Streamlit app."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    """Recommend courses based on user input."""
    st.subheader("Courses & Certificates🎓 Recommendations")
    random.shuffle(course_list)
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    for c_name, c_link in course_list[:no_of_reco]:
        st.markdown(f"- [{c_name}]({c_link})")

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    """Insert user data into the database."""
    insert_sql = """INSERT INTO user_data (Name, Email_ID, resume_score, Timestamp, Page_no, 
                    Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    rec_values = (name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def register_user(name, email, password):
    """Register a new user."""
    hashed_password = hash_password(password)
    insert_sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_sql, (name, email, hashed_password))
    connection.commit()
    st.success("Registration successful!")

# Create a directory for uploaded resumes
directory = "Uploaded_Resumes"
if not os.path.exists(directory):
    os.makedirs(directory)

def run():
    st.set_page_config(page_title="Smart Resume Analyser", page_icon='SRA_Logo.ico')
    st.title("Smart Resume Analyser")

    st.sidebar.markdown("# Choose User")
    choice = st.sidebar.selectbox("Choose among the given options:", ACTIVITIES)

    img = Image.open('SRA_Logo.jpg').resize((250, 250))
    st.image(img)

    # Create user data table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            ID INT NOT NULL AUTO_INCREMENT,
            Name varchar(100) NOT NULL,
            Email_ID VARCHAR(50) NOT NULL,
            resume_score VARCHAR(8) NOT NULL,
            Timestamp VARCHAR(50) NOT NULL,
            Page_no VARCHAR(5) NOT NULL,
            Predicted_Field VARCHAR(25) NOT NULL,
            User_level VARCHAR(30) NOT NULL,
            Actual_skills VARCHAR(300) NOT NULL,
            Recommended_skills VARCHAR(300) NOT NULL,
            Recommended_courses VARCHAR(600) NOT NULL,
            PRIMARY KEY (ID)
        );
    """)

    if choice == 'Normal User':
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            save_image_path = os.path.join(directory, pdf_file.name)
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)

            with st.spinner('Processing your resume...'):
                resume_data = ResumeParser(save_image_path).get_extracted_data()
                if resume_data:
                    analyze_resume(resume_data, save_image_path)
                else:
                    st.error('Something went wrong while parsing the resume.')
    else:
        admin_login()  # Ensure this function is implemented

def analyze_resume(resume_data, save_image_path):
    """Analyze the uploaded resume and provide recommendations."""
    st.header("Resume Analysis")
    st.success(f"Hello {resume_data.get('name', 'User')}")

    # Display basic info
    st.subheader("Your Basic info")
    st.text(f"Name: {resume_data.get('name', 'N/A')}")
    st.text(f"Email: {resume_data.get('email', 'N/A')}")
    st.text(f"Contact: {resume_data.get('mobile_number', 'N/A')}")
    st.text(f"Resume pages: {resume_data.get('no_of_pages', 0)}")

    # Candidate level determination
    candidate_levels = {
        1: "Fresher",
        2: "Intermediate",
        3: "Experienced"
    }
    level = candidate_levels.get(resume_data.get('no_of_pages', 0), "Unknown")
    st.markdown(f"<h4 style='color: #d73b5c;'>You are looking {level}.</h4>", unsafe_allow_html=True)

    # Skills recommendation
    skills_recommendation(resume_data)

    # Insert data into the database
    insert_resume_data(resume_data)

def skills_recommendation(resume_data):
    """Provide skill recommendations based on the user's resume."""
    st.subheader("Skills Analysis")
    user_skills = resume_data.get('skills', [])
    st.write("You listed the following skills:")
    st.write(user_skills)

    # Define keywords for different fields
    keywords_map = {
        'Data Science': ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit'],
        'Web Development': ['react', 'django', 'node js', 'php', 'laravel', 'javascript'],
        'Android Development': ['android', 'flutter', 'kotlin'],
        'iOS Development': ['ios', 'swift'],
        'UI/UX Design': ['ux', 'adobe xd', 'figma']
    }

    recommended_skills = []
    reco_field = ''

    for field, keywords in keywords_map.items():
        if any(skill.lower() in keywords for skill in user_skills):
            reco_field = field
            recommended_skills = [f'Explore {keyword}' for keyword in keywords]
            break

    if reco_field:
        st.success(f"Our analysis suggests you're suited for {reco_field}.")
        st.write("Recommended skills to consider developing:")
        st.write(recommended_skills)
    else:
        st.warning("No specific field identified based on your skills.")

def insert_resume_data(resume_data):
    """Insert resume data into the database."""
    name = resume_data.get('name', 'N/A')
    email = resume_data.get('email', 'N/A')
    res_score = resume_data.get('resume_score', 'N/A')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%")
