import streamlit as st
from openai import OpenAI
from PIL import Image
from rembg import remove
import io
import requests

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="AI 이모티콘 메이커", layout="centered")
st.title("🎨 나만의 상황 맞춤 이모티콘 생성기")
st.write("상황을 입력하면 AI가 배경이 제거된 이모티콘을 만들어줍니다.")

# 2. 사이드바에서 API 키 입력 (보안을 위해)
with st.sidebar:
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    st.info("기본 아바타 스타일이 적용됩니다.")

# 3. 사용자 입력
situation = st.text_input("지금 어떤 상황인가요?", placeholder="예: 전공 서적에 파묻힌 공대생")

if st.button("이모티콘 생성하기"):
    if not api_key:
        st.error("API 키를 입력해주세요!")
    elif not situation:
        st.warning("상황을 입력해주세요!")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("AI가 이미지를 생성 중입니다..."):
                # DALL-E 이미지 생성
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"A cute 3D avatar character emoticon, solid plain white background, centered, representing: {situation}. High quality, vibrant.",
                    size="1024x1024"
                )
                image_url = response.data[0].url
                raw_img = Image.open(io.BytesIO(requests.get(image_url).content))

            with st.spinner("배경을 깔끔하게 지우는 중..."):
                # 배경 제거
                processed_img = remove(raw_img)
                
                # 웹 화면에 출력
                st.image(processed_img, caption=f"생성된 이모티콘: {situation}")
                
                # 다운로드 버튼 제공
                buf = io.BytesIO()
                processed_img.save(buf, format="PNG")
                st.download_button(
                    label="이모티콘 다운로드 (PNG)",
                    data=buf.getvalue(),
                    file_name="my_emoticon.png",
                    mime="image/png"
                )
                st.success("완료! 우클릭하여 저장하거나 다운로드 버튼을 누르세요.")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
