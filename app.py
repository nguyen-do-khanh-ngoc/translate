import streamlit as st
import pandas as pd
import re
import random

# --- Định nghĩa Class Translator của bạn ---
class RuleBasedTranslator:
    def __init__(self, dictionary_df):
        self.translation_map = {}
        self._build_mapping(dictionary_df)

    def _build_mapping(self, df):
        clean_df = df.dropna(subset=["word", "meaning"])
        for _, row in clean_df.iterrows():
            key = str(row["word"]).lower().strip()
            val = str(row["meaning"]).lower().strip()
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
            # Regex bảo vệ biên từ
            pattern = r'(?<![\wàáảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ])' \
                      + re.escape(western_word) \
                      + r'(?![\wàáảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ])'
            translated_text = re.sub(pattern, vietnamese_common, translated_text)
        return re.sub(r'\s+', ' ', translated_text).strip()

# --- Giao diện Streamlit ---
def main():
    st.set_page_config(page_title="Translator App", page_icon="🤖")
    st.title("🤖 Rule-Based Translator")
    st.markdown("Công cụ dịch thuật dựa trên quy tắc đơn giản.")

    # Sidebar: Upload từ điển
    st.sidebar.header("📂 Cấu hình")
    uploaded_file = st.sidebar.file_uploader("Upload file từ điển (CSV)", type="csv")

    if uploaded_file:
        df_dict = pd.read_csv(uploaded_file)
        # Giả định file có 2 cột là 'word' và 'meaning'
        translator = RuleBasedTranslator(df_dict)
        st.sidebar.success("Từ điển đã được tải thành công!")

        # Khu vực nhập liệu
        st.subheader("Nhập văn bản cần dịch")
        input_text = st.text_area("Câu văn:", height=100)
        
        if st.button("Dịch ngay 🚀"):
            if input_text:
                output = translator.translate_sentence(input_text)
                st.subheader("Kết quả dịch:")
                st.success(output)
            else:
                st.warning("Bạn chưa nhập câu nào cả!")
    else:
        st.info("Vui lòng upload file CSV từ điển ở thanh bên trái để bắt đầu.")

if __name__ == "__main__":
    main()
