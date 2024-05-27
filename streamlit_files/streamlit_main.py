import os
import streamlit as st
from util import get_models, stream

temp_path = 'streamlit_files/temp.mp4'
st.set_page_config(page_title="Drowning Detection", layout="wide")
m_paths = [f'models/{p}' for p in os.listdir('models/')]

models = get_models(m_paths)
st.title('Drowning')

with st.sidebar:
    # confidence_threshold = st.slider('Select Model Confidence', 25, 100, 40)
    st.header("Configure Model")
    sb_col1, sb_col2 = st.columns(2)

    with sb_col1:
        model_path = st.selectbox('Select a model', m_paths)
        model = models[model_path]

        st.radio('Select a task',
                 key='usage_type',
                 options=['Streaming', 'Upload a video']
                 )

    with sb_col2:
        if st.session_state.usage_type == 'Streaming':
            st.session_state.path = 0
            st.session_state.start_button = st.button('Start Streaming from camera')
        else:
            def upload():
                if st.session_state['temp_file'] is not None:
                    with open(temp_path, 'wb') as f:
                        f.write(st.session_state['temp_file'].read())

            uploaded_file = st.file_uploader("Choose a video...",
                                             type=['mp4'],
                                             on_change=upload,
                                             key='temp_file'
                                             )

            if uploaded_file is not None:
                st.session_state.path = temp_path
                st.session_state.start_button = st.button('Start')

if st.session_state.start_button:
    st.session_state.start_button = False
    stream(model, st.session_state.path)

print(st.session_state)
