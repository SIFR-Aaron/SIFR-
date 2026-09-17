import streamlit as st
import requests

# 设置网页标题和说明
st.title("💰 汇率结算助手")
st.write("请输入你的各种货币余额，系统会自动实时折算成人民币。")

# 获取汇率（使用缓存，1小时更新一次，避免频繁请求被封锁）
@st.cache_data(ttl=3600)
def get_rates():
    try:
        url = "https://open.er-api.com/v6/latest/CNY"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["rates"]["HKD"], data["rates"]["KRW"], True
    except Exception as e:
        # 如果网络失败，使用备用汇率，保证网页不崩溃
        return 0.92, 0.0052, False 

# 获取汇率
hkd_rate, krw_rate, is_success = get_rates()

# 在侧边栏显示汇率获取状态
if is_success:
    st.sidebar.success("✅ 实时汇率获取成功！")
else:
    st.sidebar.warning("⚠️ 实时汇率获取失败，当前使用备用估算汇率！")

# 网页输入框（替代原来的 input）
st.subheader("请输入你的余额：")
港币 = st.number_input("港币余额 (HKD):", min_value=0.0, step=0.01, value=0.0)
韩元 = st.number_input("韩元余额 (KRW):", min_value=0.0, step=0.01, value=0.0)
人民币 = st.number_input("人民币余额 (CNY):", min_value=0.0, step=0.01, value=0.0)

# 实时计算总额（网页里不需要按按钮，输入框一变动，结果自动刷新）
总额 = 人民币 + (港币 / hkd_rate) + (韩元 / krw_rate)

# 显示结果
st.divider() # 画一条分割线
st.markdown(f"### 折算成人民币总额： **¥ {round(总额, 2)}**")
