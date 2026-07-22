import json

input_filename = "company_tickers.json"
output_filename = "name_company.json"

# 1. Carregar o JSON original
with open(input_filename, "r", encoding="utf-8") as file:
    data = json.load(file)

formatted_data = {}
seen_titles = set()
seen_tickers = set()

# 2. Filtrar e remover duplicados de 'title' e 'ticker'
for item in data.values():
    title = item.get("title")
    ticker = item.get("ticker")

    if title and ticker:
        # Verifica se nem o nome nem o ticker já foram adicionados
        if title not in seen_titles and ticker not in seen_tickers:
            formatted_data[title] = ticker
            seen_titles.add(title)
            seen_tickers.add(ticker)

# 3. Salvar no novo arquivo
with open(output_filename, "w", encoding="utf-8") as file:
    json.dump(formatted_data, file, ensure_ascii=False, indent=4)

print(
    f"Arquivo processado com sucesso! Total de empresas únicas: {len(formatted_data)}"
)