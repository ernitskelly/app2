import streamlit as st
from langchain import PromptTemplate
from langchain_community.llms import OpenAI
import os

template = """
 You are a marketing copywriter with 20 years of experience. You are analyzing customer's background to write personalized product description that only this customer will receive; 
    PRODUCT input text: {content};
    CUSTOMER age group (y): {agegroup};
    CUSTOMER main health_condition: {health_condition};
    TASK: Write a product description that is tailored into this customer's Age group and health_condition. Use age group specific slang.;
    FORMAT: Present the result in the following order: (PRODUCT DESCRIPTION), (BENEFITS), (USE CASE);
    PRODUCT DESCRIPTION: describe the product in 5 sentences;
    BENEFITS: describe in 3 sentences why this product is perfect considering customers age group and health_condition;
    USE CASE: write a story in 5 sentences, of an example weekend activity taking into account health_condition {health_condition} and age {agegroup}, write a story in first person, example "I started my Saturday morning with ...";
"""

prompt = PromptTemplate(
    input_variables=["agegroup", "health_condition", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Ettevõtte töötajate arv: Väike <50\nEttevõtte tegevusvaldkond: Farmatseutiliste toodete müük ja turundus\nToode: Retseptiravimid\nBränd/valmistaja: KellyPharma\nÄpi otstarve: Veebilehel kuvatavate tootetutvustustekstide personaliseerimine iga apteegikülastaja jaoks; väljundtekst on kohandatud kliendi a) terviseseisundi ja b) ravimi vajadustega; sisendtekstiks on neutraalses vormis ravimi üldine kirjeldus.\nÄriprotsess, mida äpp toetab: Turundustekstide loomine (copywriting) farmaatsiatoodetele\nÄpi kasutajad: Ettevõtte turundus- ja müügimeeskond\nÄpi kasutamise sammud: 1. Kasutaja valmistab ette ravimi kirjelduse (sisendteksti). 2. Määrab apteegikülastajatele vastavalt nende terviseseisundile ja ravivajadusele segmente. 3. Sisestab ükshaaval segmentide lõikes eeltoodud info äpi kasutajaliideses, saadab ära. 4. Kopeerib ükshaaval segmentide lõikes äpi väljundteksti vastavate ravimi tutvustuslehtede jaoks.\nÄpi eeldatav kasu (efekt): 1. Ettevõttel on võimalik pakkuda personaliseeritud ravimiteavet, mis vastab klientide individuaalsetele vajadustele ja terviseseisundile. 2. Turundus- ja müügimeeskond saab tõhusamalt luua sihitud turundustekste, mis aitavad suurendada müüki ja klientide kaasatust. 3. Kliendid saavad vastavalt oma terviseolukorrale selgemat ja kohandatud teavet ravimite kohta.")

with col2:
    st.image(image='pharmacy.jpg', caption='Pharmacy')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_agegroup = st.selectbox(
        'Which age group would you like your content to target?',
        ('9-15', '16-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100'))
    
def get_hobby():
    input_text = st.text_input(label="Customers main health_condition", key="hobby_input")
    return input_text

hobby_input = get_hobby()

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    st.session_state.content_input = "t shirts, all colors, cotton, responsible manufacturing"

st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_content = prompt.format(agegroup=option_agegroup, health_condition=hobby_input, content=content_input)
    formatted_content = llm(prompt_with_content)
    st.write(formatted_content)
