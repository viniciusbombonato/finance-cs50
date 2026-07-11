with open("company_tickers.json", "r") as f:
    f = f.json()
    companies = []

    for line in f:
        data = line.value()
        companies.append(data["title"])
    
    for company in companies:
        print(company)