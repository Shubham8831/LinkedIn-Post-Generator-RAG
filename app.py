import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Cache loading of the posts to speed up reruns
@st.cache_data
def load_tags():
    fs = FewShotPosts()
    return sorted(fs.get_tags())

def main():
    st.set_page_config(page_title="Advance LinkedIn Post Generator", layout="wide")
    st.title("💼 LinkedIn Post Generator")
    st.markdown(
        """
    Generate ready-to-go LinkedIn posts based on topic, length and language.
    """,
        unsafe_allow_html=True,
    )

    # Side bar controls
    with st.sidebar:
        st.header("Settings")
        tags = load_tags()
        selected_tag = st.selectbox("🔖 Topic", tags)
        selected_length = st.selectbox("✏️ Length", ["Short", "Medium", "Long"])
        selected_language = st.selectbox("🌐 Language", ["English", "Hinglish"])
        generate = st.button("Generate Post")

    # Show selected options in main area
    st.write("#### Your choices")
    cols = st.columns(3)
    cols[0].metric("Topic", selected_tag)
    cols[1].metric("Length", selected_length)
    cols[2].metric("Language", selected_language)

    # On-click: generate and display
    if generate:
        with st.spinner("Crafting your post…"):
            post_text = generate_post(selected_length, selected_language, selected_tag)
        st.markdown("---")
        st.subheader("🚀 Your Generated Post")
        st.write(post_text)

if __name__ == "__main__":
    main()
