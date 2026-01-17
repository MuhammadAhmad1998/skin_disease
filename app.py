import streamlit as st
import json
import base64
import numpy as np
import cv2
from openai import OpenAI
from PIL import Image
import openai,os,re
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
def encode_image(image):
    # Resize and encode the image to base64
    img = Image.fromarray(image)
    img = img.resize((320, 320))  # Resize to 640x640
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    image_data = buffer.getvalue()
    return base64.b64encode(image_data).decode('utf-8')

def extract_json(text):
    # Find all occurrences of text within curly braces
    json_strings = re.findall(r'\{.*?\}', text, re.DOTALL)
    
    json_objects = []
    for json_str in json_strings:
        try:
            # Parse the string as JSON
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Cannot Decode JSON {e}")
            continue
    
    return json_objects
def get_openai_response(image, user_symptoms):
    # Define the prompt
    prompt = f"""
        You are an AI assistant which tries to predict dermatologist issues based on the image provided, Your task is to predict the skin condition considering the symptoms described: {user_symptoms}. 
        The response should include:
        1. Name of the possible diseases.
        2. Possible causes.
        3. Recommended precautions.
        4. Suggested medications.

        Provide the output in the following JSON format (valid JSON with double-quotes):
        {{
          "name": "...",
          "causes": "...",
          "precautions": "...",
          "medications": "..."
        }}
        Instructions:
        1. Only output the JSON, nothing else.
        2. Keep in mind the symptopms when analyzing
        3. If you think there are 2 diseases then write both
        4. If symptoms are of different disease than the image then write both diseases seperated by or.
        5. Only return valid JSON.
        6. Never include backtick symbols such as: `
        7. The response will be parsed with json.loads(), therefore it must be valid JSON.
        8. You must identify the disease.
        """
    
    # Send the request to OpenAI
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image)}"
                        }
                    },
                ],
            }
        ],
        temperature=0.1,
        response_format={"type":"json_object"}
        
    )
    response=completion.choices[0].message.content
    print(response)
    # Extract and parse the JSON response
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("Went into exception")
        result_final=extract_json(response)
        return result_final


# Streamlit UI
st.title("Skin Disease Classification")
st.write("""
This application predicts skin diseases based on the image you provide and considers user-described symptoms.
""")

user_symptoms = st.text_area("Enter symptoms:", value="")
print(user_symptoms)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)
    
    # Encode the image to base64 and get OpenAI's response
    result = get_openai_response(image, str(user_symptoms))
    try:
        # Display the results
        st.subheader("Prediction Results")
        st.write(f"**Name of Disease:** {result['name']}")
        st.write(f"**Possible Causes:** {result['causes']}")
        st.write(f"**Recommended Precautions:** {result['precautions']}")
        st.write(f"**Suggested Medications (Consult a doctor):** {result['medications']}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
