import requests
import streamlit as st
import re

def format_cnpj(cnpj):
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

def format_cep(cep):
    return f"{cep[:5]}-{cep[5:]}"

def format_phone(phone):
    if len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    elif len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    return phone

def format_currency(value):
    """
    Formata valores monetários no padrão brasileiro:
    - Para valores com magnitude >= 1000, remove a parte decimal (sem vírgula), ex: 1234.56 -> R$1.234
    - Para valores < 1000, mantém duas casas decimais com vírgula, ex: 12.5 -> R$12,50
    Aceita int, float ou string que represente número. Em caso de erro retorna 'R$0'.
    """
    try:
        # converte para float (aceita int/float/strings numéricas)
        val = float(value) if value is not None and value != "" else 0.0
    except Exception:
        return "R$0"
    
    formatted = f"{val:,.2f}"  # ex: '1,234.56'
    marker = "__TH__"
    formatted = formatted.replace(",", marker)
    formatted = formatted.replace(".", ",")
    formatted = formatted.replace(marker, ".")

    return f"R${formatted}"

def format_date(date_str):
    """Converte data do formato 'YYYY-MM-DD' para 'DD/MM/YYYY'."""
    try:
        year, month, day = date_str.split("-")
        return f"{day}/{month}/{year}"
    except Exception:
        return date_str

st.set_page_config(page_title="Consulta CNPJ", layout="centered", page_icon="🏢")
st.title("Consulta CNPJ (BrasilAPI)🔎")

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
                    st.write("---")
                    st.success("Dados encontrados com sucesso!")
                    
                    st.write("---")
                    st.subheader("Informações da Empresa:")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("🏛️ **Razão Social:**")
                        st.write(data.get('razao_social', 'N/A'))
                        st.write("🏷️ **Nome Fantasia:**")
                        st.write(data.get('nome_fantasia', 'N/A'))
                        st.write("🏢 **CNPJ:**")
                        st.write(format_cnpj(data.get('cnpj', 'N/A')))
                        st.write("💰 **Capital Social:**")
                        st.write(format_currency(data.get('capital_social', 0)))
                        st.write("🗓️ **Data de Abertura:**")
                        st.write(format_date(data.get("data_inicio_atividade", "N/A")))
                        st.write("📞 **Telefones:**")
                        st.write(f"{data.get('ddd_telefone_1', 'N/A')}, {data.get('ddd_telefone_2', 'N/A')}")
                        
                    with col2:
                        st.write("📍**Endereço:**")
                        st.write(f"{data.get('descricao_tipo_de_logradouro', 'N/A')} {data.get('logradouro', 'N/A')}, {data.get('numero', 'N/A')} {data.get('complemento', 'N/A')}")
                        st.write(f"{data.get('bairro', 'N/A')} - {data.get('municipio', 'N/A')}/{data.get('uf', 'N/A')}")
                        st.write("📮**CEP:**")
                        st.write(format_cep(data.get('cep', 'N/A')))
                        st.write("📩**E-mail:**")
                        st.write(data.get('email', 'N/A'))
                        st.write("💼**Situação Cadastral:**")
                        st.write(data.get('descricao_situacao_cadastral', 'N/A'))
                        st.write("🗓️**Data da Situação Cadastral:**")
                        st.write(format_date(data.get('data_situacao_cadastral', 'N/A')))
                        st.write("📜**Regime de Tributação:**")

                        regimes = data.get('regime_tributario', [])
                        regime = regimes[-1] if regimes else None

                        st.write(regime.get('forma_de_tributacao', 'N/A') if regime else "N/A")

                    st.write("---")
                    st.subheader("🧑‍💼 Sócios:")
                    socios = data.get('qsa', [])
                    if socios:
                        for socio in socios:
                            st.write(f"- Nome: {socio.get('nome_socio', 'N/A')} ({socio.get('qualificacao_socio', 'N/A')})")
                            st.write(f"- CPF/CNPJ: {socio.get('cnpj_cpf_do_socio', 'N/A')}")
                            st.write(f"- Data de Entrada na Sociedade: {socio.get('data_entrada_sociedade', 'N/A')}")
                            st.write("---")
                    else:
                        st.write("Nenhum sócio encontrado.")

                    st.subheader("📝 Atividades:")
                    st.write("**Atividade Principal:**")
                    st.write(f"- {data.get('cnae_fiscal_descricao', 'N/A')}")

                    if data.get('cnaes_secundarios'):
                        st.write("**Atividades Secundárias:**")
                        for atividade in data.get('cnaes_secundarios'):
                            st.write(f"- {atividade.get('descricao', 'N/A')}")
                else:
                    st.error("CNPJ não encontrado na base de dados.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao consultar o CNPJ: {e}")
    else:
        st.error("Por favor, insira um CNPJ válido.")