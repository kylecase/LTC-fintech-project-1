import json


def ltc_run(*ags):
    portfolio = Element('portfolio-data')
    tickers = json.loads(portfolio.element.value)
    portfolio_imputs = tickers["covalent"]
    pyscript.write("output", portfolio_imputs)
