import streamlit as st
import pandas as pd

# Streamlit 앱 제목
st.title("학원 정보 제공 플랫폼")

# 사이드바 메뉴
menu = st.sidebar.selectbox(
    "카테고리를 선택하세요",
    ["홈", "학원 검색", "통계", "FAQ"]
)

# 데이터 불러오기
file_path = "academy.csv"

try:
    academy_df = pd.read_csv(file_path, encoding='cp949')  # 파일 로드
except FileNotFoundError:
    st.error("학원 데이터 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
    st.stop()

# 데이터 전처리: 결측치 제거
academy_df.dropna(subset=['학원명', '도로명주소'], inplace=True)

# 중복 데이터 처리: 학원명과 도로명주소 기준으로 중복 제거
academy_df.drop_duplicates(subset=['학원명', '도로명주소'], inplace=True)

# 각 카테고리별 콘텐츠 출력
if menu == "홈":
    st.write("여기서 학원 정보를 검색하고, 통계를 확인하고, 자주 묻는 질문을 볼 수 있습니다.")
    st.write("사이드에 있는 탭을 참고하여 원하는 정보를 확인하세요.")
    
    # 홈 탭에 이미지 추가
    st.image("156.jpeg", caption="학원 정보 제공 플랫폼", use_column_width=True)  # 이미지 경로와 캡션을 설정

    
elif menu == "학원 검색":
    st.subheader("학원 검색")
    # 사용자 입력: 시도교육청명 (지역명)
    region = st.text_input("지역을 입력하세요 (예: 강남구, 안동시)").strip()

    if st.button("검색", key="search_button_unique"):
        if region:
            # 입력된 지역명으로 데이터 필터링
            filtered_data = academy_df[academy_df["행정구역명"].str.contains(region, na=False)]

            # 결과 출력
            if not filtered_data.empty:
                st.success(f"{len(filtered_data)}개의 학원을 찾았습니다.")
                for _, row in filtered_data.iterrows():
                    st.subheader(row["학원명"])
                    st.write(f"교습과정: {row['분야명']}")
                    st.write(f"주소: {row['도로명주소']}")
                    st.write(f"전화번호: {row['전화번호']}")
                    st.write(f"개설일자: {row['개설일자']}")
                    st.write("---")
            else:
                st.warning("검색 결과가 없습니다.")
        else:
            st.warning("지역명을 입력하세요.")

elif menu == "통계":
    st.subheader("학원 통계")
    # 예를 들어, 지역별 학원 수를 시각화하는 코드
    region_count = academy_df['행정구역명'].value_counts().reset_index()
    region_count.columns = ['행정구역명', '학원 수']

    st.write(region_count)

elif menu == "FAQ":
    st.subheader("자주 묻는 질문")
    st.write("1. 이 플랫폼은 어떤 데이터를 제공하나요?")
    st.write("          - 공공 데이터를 기반으로 학원 정보를 제공합니다.")
    st.write("2. 어떻게 학원을 찾을 수 있나요?")
    st.write("          - 지역명을 입력하여 학원을 검색할 수 있습니다.")
