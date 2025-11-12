# BUSCA-CNPJ

Aplicação simples em Streamlit para consultar dados de empresas brasileiras a partir do CNPJ
usando a API pública BrasilAPI.

## O que faz

- Permite inserir um CNPJ e obter informações como razão social, nome fantasia, capital social,
	endereço, sócios, atividades e regime de tributação.
- Formata valores monetários no padrão brasileiro: separador de milhares com `.` e decimais com `,`.
	Exemplo: `R$1.234,56`.

## Requisitos

- Python 3.8+ (recomendado)
- Dependências listadas no `pyproject.toml` (ou instale manualmente): `streamlit`, `requests`

## Como rodar

1. Crie e ative um ambiente virtual (opcional, recomendado):

```bash
python -m venv .venv
source .venv/bin/activate   # no Windows (bash): .venv\Scripts\activate
```

2. Instale dependências:

```bash
pip install streamlit requests
```

3. Rode a aplicação:

```bash
streamlit run main.py
```

4. Acesse a interface no navegador (geralmente em `http://localhost:8501`).

## Observações importantes

- A aplicação consulta a API pública `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`. Caso a API esteja
	indisponível ou limitada, a consulta pode falhar.
- A formatação de `capital_social` e outros valores monetários foi ajustada para seguir o padrão brasileiro
	(milhares com ponto e decimais com vírgula), e os centavos são sempre exibidos, ex: `R$1.000,00`.

## Exemplos de formatação

- 12.5  -> `R$12,50`
- 1000.0 -> `R$1.000,00`
- 1234567.89 -> `R$1.234.567,89`

## Estrutura do projeto

- `main.py` - código da aplicação Streamlit
- `README.md` - este arquivo

## Próximos passos sugeridos

- Adicionar testes unitários para a função `format_currency`.
- Tratar e exibir melhor telefones (normalização / formatos faltantes).
- Armazenar consultas em cache para evitar muitas chamadas à API.

---
Feito como projeto de estudo.
