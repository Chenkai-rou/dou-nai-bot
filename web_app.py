import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="豆族掌门直播间", page_icon="💋")
st.title("💋 豆族掌门：豆奶大王")

# ---------------------------------------------------------
# 👇 这里改了：尝试从后台秘密保险箱里获取 Key
# ---------------------------------------------------------
try:
    # 优先使用后台配置的 Key (Secrets)
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    # 如果后台没配置（比如你在本地运行），才显示输入框
    api_key = st.sidebar.text_input("请输入 DeepSeek API Key", type="password")

# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("输入弹幕，撩一下豆奶大王...")

if user_input:
    if not api_key:
        st.toast("🚫 哎呀，没有密钥，豆奶大王不想理你！")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        # (这里省略了 Prompt，你可以把之前那个精彩的“豆族掌门” Prompt 粘回来)
        # 为了演示简洁，我先写个简单的，你记得换回你的“豆奶大王”版
        system_prompt = "你是豆奶大王，说话要骚气，叫用户哥哥。" 

        with st.chat_message("assistant"):
            with st.spinner("💋 豆奶大王正在整理发型..."):
                try:
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.messages 
                        ]
                    )
                    result = response.choices[0].message.content
                    st.write(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                except Exception as e:
                    st.error(f"出错啦：{e}")