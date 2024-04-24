import os

from openai import OpenAI
import textwrap


def translate_text_for_image(text):
    client = OpenAI(
        api_key=os.getenv("OPENAI_KEY")
    )

    user_content = f"Translate the following Korean sentences into English\n {text}"
    messages = [{"role": "user", "content": user_content}]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
        temperature=0.8,
        n=1
    )

    reply = response.choices[0].message.content

    return reply


def generate_text_for_img(text):
    client = OpenAI(
        api_key=os.getenv("OPENAI_KEY")
    )

    user_content = f"Describe the following in 1000 characters to create an image.\n {text}"
    messages = [{"role": "user", "content": user_content}]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
        temperature=0.8,
        n=1
    )

    reply = response.choices[0].message.content

    return reply


def generate_image_from_text(text_for_img, img_num=1, img_size="512x512"):
    client = OpenAI(
        api_key=os.getenv("OPENAI_KEY")
    )
    storten_text_for_img = textwrap.shorten(text_for_img, 99)

    response = client.images.generate(
        model="dall-e-2",
        prompt=storten_text_for_img,
        size=img_size,
        n=img_num
    )

    img_urls = []

    for i in response.data:
        img_urls.append(i.url)

    return img_urls
