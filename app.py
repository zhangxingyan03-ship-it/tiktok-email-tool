import streamlit as st
import pandas as pd
import re
import requests
import time


st.title("TikTok Creator Email Finder")

uploaded_file = st.file_uploader(
    "上传 TikTok 达人名单 Excel",
    type=["xlsx"]
)


def clean_email(email):

    if not email:
        return ""

    email = email.replace("\\u002F", "")
    email = email.replace("\\/", "")
    email = email.strip()

    email = email.strip(
        " \n\t,.;:()[]{}<>\"'"
    )

    return email



def find_email(text):

    if not text:
        return ""

    text = text.replace(
        "example@example.com",
        ""
    )

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if emails:
        return clean_email(emails[0])

    return ""



def check_tiktok(user_id):

    url = f"https://www.tiktok.com/@{user_id}"

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        email = find_email(
            response.text
        )

        return email, url


    except:

        return "", url



if uploaded_file:


    df = pd.read_excel(
        uploaded_file
    )


    st.write(
        "读取成功，共",
        len(df),
        "个达人"
    )


    if st.button("开始查询邮箱"):


        results=[]

        progress = st.progress(0)


        for i, user_id in enumerate(df.iloc[:,0]):

            user_id = str(
                user_id
            ).strip()


            email, url = check_tiktok(
                user_id
            )


            results.append(
                {
                    "TikTok ID": user_id,
                    "Email": email,
                    "Profile": url
                }
            )


            time.sleep(1)


            progress.progress(
                (i+1)/len(df)
            )


        result_df = pd.DataFrame(
            results
        )


        file_name = "邮箱查询结果.xlsx"


        result_df.to_excel(
            file_name,
            index=False
        )


        st.success(
            "完成！"
        )


        with open(
            file_name,
            "rb"
        ) as f:

            st.download_button(
                "下载结果Excel",
                f,
                file_name
            )

