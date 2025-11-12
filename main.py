import requests
import streamlit as st
import re

def format_cnpj(cnpj):
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

st.set_page_config(page_title="Consulta CNPJ", layout="centered", page_icon="🏢")
st.title("Consulta CNPJ (BrasilAPI)")

st.markdown("Digite um CNPJ válido para consultar informações da empresa correspondente.")

cnpj_input = st.text_input("CNPJ: ", help="Aceita CNPJ com pontos, barras e traços ou apenas números.")

if st.button("Buscar"):
    if cnpj_input:
        conpj_clean = re.sub(r'\D', '', cnpj_input)
        if len(conpj_clean) != 14:
            st.error("CNPJ inválido. Certifique-se de que o CNPJ possui 14 dígitos.")
        else:
            try:
                api_url = f'https://brasilapi.com.br/api/cnpj/v1/{conpj_clean}'
                api_response = requests.get(api_url)
                if api_response.status_code == 200:
                    data = api_response.json()
                    st.success("Dados encontrados com sucesso!")
                    
                    st.subheader("Informações da Empresa")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**Razão Social:** {data.get('razao_social', 'N/A')}")
                        st.markdown(f"**Nome Fantasia:** {data.get('nome_fantasia', 'N/A')}")
                        st.write("**CNPJ:**")
                        st.write(format_cnpj(data.get('cnpj', 'N/A')))
                        st.write("**Capital Social**:")
                        st.write(f"R${data.get('capital_social', 0):,.2f}")
                        
                    with col2:
                        st.markdown(f"**Data de Abertura:** {data.get('data_abertura', 'N/A')}")
                        st.markdown(f"**Situação Cadastral:** {data.get('situacao_cadastral', 'N/A')}")
                        st.markdown(f"**Natureza Jurídica:** {data.get('natureza_juridica', 'N/A')}")
                        st.markdown(f"**Telefone:** {data.get('telefone', 'N/A')}")
                        st.markdown(f"**E-mail:** {data.get('email', 'N/A')}")
                else:
                    st.error("CNPJ não encontrado na base de dados.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao consultar o CNPJ: {e}")