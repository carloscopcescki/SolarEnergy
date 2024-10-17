import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import streamlit.components.v1 as components
from commands import *

# Importar a biblioteca GSEE para fazer os cálculos do painel fotovoltaico
def main() -> None:
    '''Create dashboard page'''
    st.set_page_config(
        page_title='Solar Dash',
        page_icon=':sunrise:',
        layout='wide'
    )
    
    st.html(
        '''
        <style>
        hr {
            border-color: #6495ED;
            border-radius: 100px;
        }
        </style>
        '''
    )
        
    # Sidebar elements
    st.sidebar.empty()
    st.sidebar.image('./img/fsa.png', width=230)
    
    # Input values
    search_location = st.sidebar.text_input("Pesquise um endereço", placeholder="Insira uma localização", value="FSA - Anexo II")

    panel_qty = st.sidebar.slider("Painéis solares", 0, 150, 10)
    panel_potencial = st.sidebar.number_input("Potência do painel solar (em Wp)", min_value=0, value=400)
    solar_irrad_generate = st.sidebar.number_input("Irradiação solar (em kWh/m².dia)", min_value=0.0, value=4.53)
    sys_efficiency_generate = st.sidebar.number_input("Eficiência do sistema (%)", key='efficiency-generated', min_value=0, max_value=100, step=5, value=80)
    day_generate = st.sidebar.number_input("Número de dias", key='days-generated', min_value=1, max_value=365, step=1, value=30)
    tilt = st.sidebar.slider("Inclinação do painel solar (em graus)", 0.0, 90.00, 20.00)
    azimuth = st.sidebar.slider("Orientação do painel (em graus)", -180, 180, 180)

    st.sidebar.divider()
 
    energy_consumption = st.sidebar.number_input("Consumo anual de energia (em kWh)", key='consumption', min_value=0, value=3000)
    cost_system = st.sidebar.number_input("Custo do sistema (R$)", key='cost_install', min_value=0.0, value=10000.00)
    cost_kwh = st.sidebar.number_input("Custo por kWh (R$)", key='cost_kwh', min_value=0.0, value=0.65)

    # Main elements
    calculate = EnergyCalculate()
    location = Geolocator(search_location)
    result = location.result()
    st.title("Solar Dash")
    st.subheader("Dados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(label="Energia gerada por painel", value=f"{calculate.generate(panel_potencial, solar_irrad_generate, sys_efficiency_generate, int(day_generate))}kWh")
    col2.metric(label="Capacidade gerada pelo sistema", value=f"{calculate.capacity(panel_qty)}kWh")
    col3.metric(label="Quantidade de painéis", value=panel_qty)
    col4.metric(label="Payback aproximado", value=f"{calculate.payback(cost_system, cost_kwh)} anos")
    style_metric_cards(border_left_color='#6495ED')
    
    st.divider()

    # Map
    col1a, col2a = st.columns(2)

    with col1a:
        st.subheader("Mapa")
        if search_location == "":
            st.warning("Insira um endereço no campo localização")
        else:
            if result and search_location != "FSA - Anexo II":
                lat, lon = result['geometry']['lat'], result['geometry']['lng']
                map_location = Map(lat, lon)
                map_location.map_generate()
                st.link_button("Relatório Atlas Global", "https://globalsolaratlas.info/detail?c=-23.661511,-46.55495,11&s=-23.661511,-46.55495&m=site")  
            else:
                fsa_lat = '-23.6622'
                fsa_lon = '-46.5541'
                map_location = Map(fsa_lat, fsa_lon)
                map_location.map_generate()
                st.link_button("Relatório Atlas Global", f"https://globalsolaratlas.info/detail?c={fsa_lat},{fsa_lon},11&s={fsa_lat},{fsa_lon}&m=site")

    # Solar energy production chart
    with col2a:
        st.subheader("Energia gerada")
        if result and search_location != "FSA - Anexo II":
            lat, lon = result['geometry']['lat'], result['geometry']['lng']
            energy_chart = calculate.energy_generated_chart(lat, lon, azimuth, tilt)
        else:
            energy_chart = calculate.energy_generated_chart(-23.6622, -46.5541, azimuth, tilt)

if __name__ == "__main__":
    main()
