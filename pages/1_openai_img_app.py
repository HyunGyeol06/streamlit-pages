from modules import img_gen_module
import streamlit as st
import requests
import textwrap
from datetime import datetime

if 'img_caption' not in st.session_state:
    st.session_state['img_caption'] = ""

if 'shorten_text_for_img' not in st.session_state:
    st.session_state['shorten_text_for_img'] = ""

if 'img_urls' not in st.session_state:
    st.session_state['img_urls'] = []

if 'imgs' not in st.session_state:
    st.session_state['imgs'] = []

if 'download_file_names' not in st.session_state:
    st.session_state['download_file_names'] = []

if 'download_buttons' not in st.session_state:
    st.session_state['download_buttons'] = False


def display_result():
    shorten_text_for_img = st.session_state['shorten_text_for_img']
    img_caption = st.session_state['img_caption']
    img_urls = st.session_state['img_urls']

    st.sidebar.write("[이미지 생성을 위한 텍스트]")
    st.sidebar.write(shorten_text_for_img)

    for k, img_url in enumerate(img_urls):
        st.image(img_urls, caption=img_caption)

        img_data = st.session_state['imgs'][k]
        download_file_name = st.session_state['download_file_names'][k]

        st.download_button(
            label='이미지 파일 다운로드',
            data=img_data,
            file_name=download_file_name,
            mime='image/png',
            key=k,
            on_click=download_button_callback
        )


# =================== callback function =================

def download_button_callback():
    st.session_state['download_buttons'] = True


def button_callback():
    if radio_selected_lang == "한국어":
        translated_text = img_gen_module.translate_text_for_image(input_text)
    elif radio_selected_lang == "영어":
        translated_text = input_text

    if detail_desc == "Yes":
        resp = img_gen_module.generate_text_for_img(translated_text)
        text_for_img = resp
        img_caption = "상세 묘사를 추가해 생성한 이미지"
    elif detail_desc == "No":
        text_for_img = translated_text
        img_caption = "입력 내용으로 생성한 이미지"

    shorten_text_for_img = textwrap.shorten(text_for_img, 200, placeholder='[..And So More..]')

    img_urls = img_gen_module.generate_image_from_text(text_for_img, img_num, img_size)

    imgs = []
    download_file_names = []
    for k, img_url in enumerate(img_urls):

        r = requests.get(img_url)
        img_data = r.content
        imgs.append(img_data)

        now_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        download_file_name = f"gen_image_{k}_{now_datetime}.png"
        download_file_names.append(download_file_name)

    st.session_state['img_caption'] = img_caption
    st.session_state['shorten_text_for_img'] = shorten_text_for_img
    st.session_state['img_urls'] = img_urls
    st.session_state['download_file_names'] = download_file_names
    st.session_state['imgs'] = imgs


# ===================== sidebar =======================

st.set_page_config(page_title="img_gen")


st.title("이미지 생성을 위한 설정")

input_text = st.text_input("이미지 생성을 위한 설명을 입력하세요",
                                   "빌딩이 보이는 호수가 있는 도시의 공원")

radio_selected_lang = st.radio("입력한 언어", ['한국어', '영어'], index=0, horizontal=True)

img_num_options = [1,2,3]
img_num = st.radio("생성할 이미지 개수를 선택하세요.", img_num_options, index=0, horizontal=True)

img_size_options = ["256x256", "512x512", "1024x1024"]
img_size = st.radio("생성할 이미지 크기를 선택하세요.", img_size_options, index=1, horizontal=True)

detail_desc = st.radio("상세 묘사를 추가하겠습니까?", ["Yes", "No"], index=1, horizontal=True)

clicked = st.button("이미지 생성", on_click=button_callback)

# ================== main page ================

st.title("AI 이미지 생성기")

if clicked or st.session_state['download_buttons'] == True:
    display_result()