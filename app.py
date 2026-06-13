import streamlit as st
import pandas as pd
import re
import random

# --- Class Translator ---
class RuleBasedTranslator:
    def __init__(self, dictionary_df):
        self.translation_map = {}
        self._build_mapping(dictionary_df)

    def _build_mapping(self, df):
        # Lấy 2 cột đầu bất chấp tên cột là gì
        df = df.iloc[:, [0, 1]]
        df.columns = ["Từ", "Ý nghĩa"]
        clean_df = df.dropna(subset=["Từ", "Ý nghĩa"])

        for _, row in clean_df.iterrows():
            key = str(row["Từ"]).lower().strip()
            val = str(row["Ý nghĩa"]).lower().strip()
            raw_meanings = re.split(r',|\b\d+[\.\)]\s*', val)
            meanings_list = [m.replace(".", "").strip(" ;") for m in raw_meanings if m.replace(".", "").strip(" ;")]
            if not meanings_list: meanings_list = [key]
            self.translation_map[key] = meanings_list
        self.sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)

    def translate_sentence(self, text):
        if not text: return ""
        translated_text = text.lower().strip()
        for western_word in self.sorted_keys:
            meanings_list = self.translation_map[western_word]
            vietnamese_common = random.choice(meanings_list)
            pattern = r'(?<![\wàáảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ])' \
                      + re.escape(western_word) \
                      + r'(?![\wàáảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ])'
            translated_text = re.sub(pattern, vietnamese_common, translated_text)
        return re.sub(r'\s+', ' ', translated_text).strip()

# --- Giao diện Streamlit ---
st.set_page_config(page_title="Translator App", layout="centered")
st.title("🤖 Rule-Based Translator")
st.write("Ứng dụng dịch thuật dựa trên quy tắc (Rule-based).")

# Sidebar để upload file
st.sidebar.header("Cấu hình")
uploaded_file = st.sidebar.file_uploader("Upload file từ điển (CSV)", type="csv")

if uploaded_file:
    df_dict = pd.read_csv(uploaded_file)
    translator = RuleBasedTranslator(df_dict)
    st.sidebar.success("Từ điển đã sẵn sàng!")

    input_text = st.text_area("Nhập câu cần dịch:")
    
    if st.button("Dịch ngay"):
        if input_text:
            result = translator.translate_sentence(input_text)
            st.success("Kết quả:")
            st.write(f"### {result}")
        else:
            st.warning("Vui lòng nhập văn bản.")
else:
    st.info("👈 Hãy upload file từ điển CSV ở thanh bên trái.")
