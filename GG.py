import streamlit as st
import requests
import pandas as pd

# 쿠키 및 헤더 설정
cookies = {
    'NNB': '6B6AOBVST4FF6',
    'ASID': '7df0125e000001734d9e5ce800000063',
    'NAC': 'cDYXBQgybpWb',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '4800000000',
    '_fwb': '89PXP8Ho8ngxyWJNntFp6S.1735794340196',
    'landHomeFlashUseYn': 'Y',
    'realestate.beta.lastclick.cortar': '4100000000',
    'NACT': '1',
    'page_uid': 'i3PcTwqo1fssssNlWadssssssgh-298109',
    'REALESTATE': 'Fri%20Jan%2003%202025%2016%3A24%3A18%20GMT%2B0900%20(Korean%20Standard%20Time)',
    'BUC': 'aXI_cS0J8nBrhYDCISNARMco0zWKNkXOATOV8mWxSWU=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MzU4ODkwNTgsImV4cCI6MTczNTg5OTg1OH0.t02O3-7AYxkwMJL3ppt0F2KLwqCKnOZ7E82D5_eFlcQ',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/rooms?ms=37.6426034,126.6695569,17&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&b=B2&e=RETAIL&aa=SMALLSPCRENT',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

st.title('김포시 장기동 원룸 매물 조회')

# 페이지 번호 입력받기
page_numbers = st.slider("페이지 선택", min_value=1, max_value=20, value=1)

if st.button("조회 시작"):
    all_articles = []

    for page in range(1, page_numbers + 1):
        st.write(f"페이지 {page} 요청 중...")
        response = requests.get(
            f'https://new.land.naver.com/api/articles?cortarNo=4157010400&order=rank&realEstateType=APT%3AOPST%3AABYG%3AOBYG%3AGM%3AOR%3AVL%3ADDDGG%3AJWJT%3ASGJT%3AHOJT&tradeType=B2&tag=%3A%3A%3A%3A%3A%3A%3ASMALLSPCRENT%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&articleState',
            cookies=cookies,
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            all_articles.extend(data['articleList'])
            st.write(f"페이지 {page} 데이터 저장 완료.")
        else:
            st.write(f"페이지 {page} 요청 실패:", response.status_code)

    # 수집한 데이터 프레임 생성 및 표시
    if all_articles:
        df = pd.DataFrame(all_articles)
        st.write(df[['articleNo', 'articleName', 'articleStatus', 'tradeTypeName', 'floorInfo', 'rentPrc', 'direction', 'area1', 'realtorName', 'cpPcArticleUrl']])
        st.success("모든 데이터가 성공적으로 로드되었습니다.")
    else:
        st.warning("데이터가 없습니다.")