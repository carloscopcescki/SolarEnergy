import streamlit as st
from commands import *

def main():
    '''Create dashboard page'''
    st.set_page_config(
        page_title='Solar Dash',
        page_icon=':sunrise:',
        layout='wide'
    )
    
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.image('./img/fsa.png', use_column_width=True)
    st.sidebar.title("FSA - Solar Dash")
    st.sidebar.write("Dashboard desenvolvido para exibir quantidade necessária de painés solares na FSA + potencial energético da região.")
    st.sidebar.divider()

    st.sidebar.title("Inserir dados")
    panel_potencial = st.sidebar.number_input("Potência do painel solar (em kW)", min_value=0)
    solar_irradiation = st.sidebar.number_input("Irradiação solar (em kWh/m².dia)", min_value=0)
    system_efficiency = st.sidebar.number_input("Eficiência do sistema (%)", min_value=0, max_value=100, step=5)
    irradiation_days = st.sidebar.number_input("Número de dias", min_value=1, max_value=365, step=1)

    # Main elements
    col1, col2 = st.columns(2)
    
    with col1:
        st.title("Dados")
    with col2:
        st.title("Mapa")
        with open('irradiacao_media_abc.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        st.components.v1.html(html_content, width=700, height=600)
    
if __name__ == "__main__":
    '''Start dashboard page'''
    main()
