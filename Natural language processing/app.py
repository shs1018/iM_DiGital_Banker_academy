import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_models():
    # Load Korean model
    ko_tokenizer = AutoTokenizer.from_pretrained("skt/kogpt2-base-v2")
    ko_model = AutoModelForCausalLM.from_pretrained("skt/kogpt2-base-v2")
    
    # Load English model
    en_tokenizer = AutoTokenizer.from_pretrained("gpt2")
    en_model = AutoModelForCausalLM.from_pretrained("gpt2")
    
    return (ko_tokenizer, ko_model), (en_tokenizer, en_model)

def generate_text(text, tokenizer, model, max_length=50, temperature=0.7):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        temperature=temperature
    )
    
    return tokenizer.decode(output[0], skip_special_tokens=True)

def main():
    st.title("Text Generation App 📝")
    
    # Initialize session state for generated texts
    if 'ko_generated' not in st.session_state:
        st.session_state.ko_generated = ""
    if 'en_generated' not in st.session_state:
        st.session_state.en_generated = ""
    
    # Load models
    (ko_tokenizer, ko_model), (en_tokenizer, en_model) = load_models()
    
    # Korean Section
    st.header("한국어 텍스트 생성")
    ko_text = st.text_input("입력 텍스트:", "오늘 날씨가", key="ko_input")
    
    ko_col1, ko_col2 = st.columns(2)
    with ko_col1:
        ko_max_length = st.slider("최대 길이:", 10, 200, 50, key="ko_length")
    with ko_col2:
        ko_temperature = st.slider("다양성:", 0.1, 1.0, 0.7, key="ko_temp")
    
    if st.button("텍스트 생성", key="ko_button"):
        with st.spinner("생성 중..."):
            st.session_state.ko_generated = generate_text(
                ko_text,
                ko_tokenizer,
                ko_model,
                max_length=ko_max_length,
                temperature=ko_temperature
            )
    
    if st.session_state.ko_generated:
        st.success("생성 완료!")
        st.write("생성된 텍스트:")
        st.write(st.session_state.ko_generated)
    
    # Divider
    st.markdown("---")
    
    # English Section
    st.header("English Text Generation")
    en_text = st.text_input("Input text:", "The weather today is", key="en_input")
    
    en_col1, en_col2 = st.columns(2)
    with en_col1:
        en_max_length = st.slider("Maximum Length:", 10, 200, 50, key="en_length")
    with en_col2:
        en_temperature = st.slider("Temperature:", 0.1, 1.0, 0.7, key="en_temp")
    
    if st.button("Generate Text", key="en_button"):
        with st.spinner("Generating..."):
            st.session_state.en_generated = generate_text(
                en_text,
                en_tokenizer,
                en_model,
                max_length=en_max_length,
                temperature=en_temperature
            )
    
    if st.session_state.en_generated:
        st.success("Generation Complete!")
        st.write("Generated Text:")
        st.write(st.session_state.en_generated)

if __name__ == "__main__":
    main()
