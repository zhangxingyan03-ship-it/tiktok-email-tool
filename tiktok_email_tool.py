import pandas as pd
import re
import requests
from tqdm import tqdm
import time


INPUT_FILE = "TikTok达人名单.xlsx"
OUTPUT_FILE = "邮箱查询结果.xlsx"


def clean_email(email):

    if not email:
        return ""

    # 清理TikTok网页编码
    email = email.replace("\\u002F", "")
    email = email.replace("\\/", "")
    email = email.strip()

    # 去掉邮箱前后的无效符号
    email = email.strip(
        " \n\t,.;:()[]{}<>\"'"
    )

    return email



def find_email(text):

    if not text:
        return ""


    # 删除TikTok测试邮箱
    text = text.replace(
        "example@example.com",
        ""
    )


    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )


    if emails:

        email = clean_email(
            emails[0]
        )

        return email


    return ""



def check_tiktok(user_id):

    url = f"https://www.tiktok.com/@{user_id}"


    try:

        headers = {

            "User-Agent":
            (
                "Mozilla/5.0 "
                "(Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "Chrome/120 Safari/537.36"
            ),

            "Accept-Language":
            "en-US,en;q=0.9"

        }


        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )


        text = response.text


        email = find_email(text)


        return email, url



    except Exception as e:

        print(
            "错误:",
            user_id,
            e
        )

        return "", url




# 读取达人名单

df = pd.read_excel(
    INPUT_FILE
)


results = []


seen = set()



for user_id in tqdm(
    df["Tik Tok ID"]
):

    user_id = str(
        user_id
    ).strip()


    email, url = check_tiktok(
        user_id
    )


    # 邮箱去重
    if email:
        if email in seen:
            email = ""

        else:
            seen.add(email)



    results.append(
        {
            "TikTok ID": user_id,
            "Email": email,
            "Profile": url
        }
    )


    time.sleep(1)



result_df = pd.DataFrame(
    results
)


result_df.to_excel(
    OUTPUT_FILE,
    index=False
)


print(
    "完成！已生成：",
    OUTPUT_FILE
)
