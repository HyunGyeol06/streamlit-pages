from openai import OpenAI
import streamlit as st
import deepl
import tiktoken


def summarize_text(user_text, lang='en'):
    client = OpenAI(
        api_key=st.secrets["openai_key"]
    )

    if lang == "en":
        messages = [
            {"role": "system", "content": "You are a helpful assistant in the summary."},
            {"role": "user", "content": f"Summarize the following. \n {user_text}"}
        ]
    elif lang == "ko":
        messages = [
            {"role": "system", "content": "You are a helpful assistant in the summary."},
            {"role": "user", "content": f"다음의 내용을 한국어로 요약해 주세요.\n {user_text}"}
        ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2000,
        temperature=0.3,
    )
    summary = response.choices[0].message.content
    return summary


def summarize_text_final(text_list, lang="en"):
    joined_summary = " ".join(text_list)

    enc = tiktoken.encoding_for_model("gpt-4")
    token_num = len(enc.encode(joined_summary))

    req_max_token = 2000
    final_summary = ""
    if token_num < req_max_token:
        final_summary = summarize_text(joined_summary, lang)

    return token_num, final_summary


def translate_english_to_korean_by_openAI(text):
    client = OpenAI(
        api_key=st.secrets["openai_key"]
    )
    user_content = f"Translate the following English sentences tnto Korean.\n {text}"
    messages = [{"role":"user", "content":user_content}]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2000,
        temperature=0.3,
        n =1
    )
    reply = response.choices[0].message.content

    return reply


def translate_english_to_korean_by_deepL(text):
    auth_key = st.secrets["deepl_key"]
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang="KO")

    return result.text
