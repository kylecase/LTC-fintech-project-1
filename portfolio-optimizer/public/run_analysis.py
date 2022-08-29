import json
from js import XMLHttpRequest
import pandas as pd
from MCForecastTools import MCSimulation
import matplotlib


def ltc_run(*ags):
    portfolio = Element('portfolio-data')
    tickers = json.loads(portfolio.element.value)
    portfolio_imput = tickers["covalent"]
    portfolio_df = pd.DataFrame()

    # initialize variables
    df_dict = {}
    mc_dict = {}
    line_plot_dict = {}
    simulated_returns_data_dict = {}

    req = XMLHttpRequest.new()
    req.open("GET", "/api/alpaca/tokens", False)
    req.send(None)
    response_coin_list = json.loads(req.response)
    coin_table_ticker = response_coin_list['data']['items']

    # create dataframe
    coin_table_df = pd.DataFrame(coin_table_ticker)

    # Data Cleanup - Check Nulls
    coin_table_df.isnull().sum()

    # Finding the total rows needed to pair the list down to 200 rows
    df_len = len(coin_table_df.index)
    drop_len = df_len - 200

    # Converting numbers saved as string to float
    coin_table_df['total_volume_24h'] = coin_table_df['total_volume_24h'].astype(
        float)
    coin_table_df['total_liquidity'] = coin_table_df['total_liquidity'].astype(
        float)
    coin_table_df['quote_rate'] = coin_table_df['quote_rate'].astype(float)
    coin_table_df['total_liquidity_quote'] = coin_table_df['total_liquidity_quote'].astype(
        float)
    coin_table_df['total_volume_24h_quote'] = coin_table_df['total_volume_24h_quote'].astype(
        float)

    # Created list of tickers to us as options that can be searched to build custom portfolio
    ticker_symbol_list = coin_table_df['contract_ticker_symbol'].tolist()

    # Created dictionary with ticker name: contract name to have if needed
    ticker_name_dict = dict(
        zip(coin_table_df.contract_ticker_symbol, coin_table_df.contract_name))

    # Created a dictionary with ticker: contact address to use in the price history API pull
    ticker_contract_dict = dict(
        zip(coin_table_df.contract_ticker_symbol, coin_table_df.contract_address))

    # Created a refrence list of tickers submitted
    ticker_list = list(portfolio_imput.keys())

    # Check len of ticker list to use to set the count variable
    len_ticker_list = len(ticker_list)
    count = len_ticker_list - 1

    # Created a list of weights that pairs with tickers in ticker_list
    weight_list = list(portfolio_imput.values())

    # Created a dict that refrences the master ticker_contract_dict to pull only our portfolio ticker contract addresses
    portfolio_contact_dict = {
        your_key: ticker_contract_dict[your_key] for your_key in portfolio_imput.keys()}

    # While Loop to pull prices for every ticker symbol from covalent api
    while count > -1:
        # Set ref = count to use ref to call the current ticker symbol being used from ticker_list
        ref = count
        count += -1
        contract_id = portfolio_contact_dict[ticker_list[ref]]

        nextReq = XMLHttpRequest.new()
        nextReq.open("GET", f"/api/alpaca/historical/{contract_id}", False)
        nextReq.send(None)
        response_coin_price = json.loads(nextReq.response)
        print(response_coin_price)

        # Create a temporary dataframe to store the returned price data
        coin_price_table = response_coin_price['data'][0]['prices']
        coin_price_df = pd.DataFrame(coin_price_table)

        # Checks to see if the dataframe is empty, if there is no price history continues from the top of the while loop
        if coin_price_df.empty:
            continue
        else:
            # Changes index to date, cleans data, sets column name to ticker symbol
            coin_price_df.set_index('date', inplace=True)
            coin_price_df.sort_index(inplace=True)
            coin_price_df.drop(columns='contract_metadata', inplace=True)
            coin_price_df['price'] = coin_price_df['price'].astype(float)
            coin_price_df.rename(
                columns={'price': ticker_list[ref]}, inplace=True)

            # If the permanant price colelction dataframe is empty replace it, otherwise merch the temp dataframe to permanant
            if portfolio_df.empty:
                portfolio_df = coin_price_df
            else:
                portfolio_df = pd.concat([portfolio_df, coin_price_df], axis=1)

            df_dict = {**df_dict, **{
                ticker_list[ref]: coin_price_df
            }}

    # Creates a string of headers from portfolio_df to compare to the original ticker_list to see what we couldn't find data for
    found_history = list(portfolio_df.columns)
    found_history_string = ' '
    found_history_string = found_history_string.join(found_history)
    found_history_string = found_history_string.replace(' ', ', ')

    no_history = list(set(ticker_list) ^ set(found_history))
    no_history_string = ' '
    no_history_string = no_history_string.join(no_history)
    no_history_string = no_history_string.replace(' ', ', ')
    print(
        f'Unfortunatly we were unable to pull history for the following tickers: {no_history_string}. Your portfolio optimizer will continue with the following tickers: {found_history_string}.')

    portfolio_weight_dict = {
        your_key: portfolio_imput[your_key] for your_key in found_history}

    imput_df = pd.DataFrame.from_dict(
        portfolio_imput, orient='index', dtype=float, columns=['weights'])
    imput_df = imput_df.drop(no_history)
    new_weights_total = imput_df['weights'].sum()
    imput_df['new_weight_pct'] = round(imput_df.weights / new_weights_total, 2)
    imput_df = imput_df.reindex(found_history)
    new_weights = list(imput_df.new_weight_pct)

    x = 0

    while x < len(df_dict):
        df_dict[str(found_history[x])].columns = pd.MultiIndex.from_product(
            [df_dict[str(found_history[x])].columns, ['close']])
        #df_dict[str(found_history[x])].rename(columns={str(found_history[x]):'close'}, inplace=True, level=0)
        #df_dict[str(found_history[x])]['symbol'] = str(found_history[x])
        #df_dict[str(found_history[x])] = df_dict[str(found_history[x])][df_dict[str(found_history[x])]['symbol']==str(found_history[x])].drop('symbol', axis=1)
        x += 1

    num_sims = 500
    mc_dict = df_dict
    num_sims = 500
    x = 0
    while x < len(df_dict):
        mc_dict[str(found_history[x])] = MCSimulation(
            portfolio_data=mc_dict[str(found_history[x])],
            num_simulation=num_sims,
            num_trading_days=365
        )
        #mc_dict[str(found_history[x])] = mc_dict[str(found_history[x])].calc_cumulative_return()
        x += 1

    x = 0
    while x < len(df_dict):
        line_plot_dict[str(found_history[x])] = mc_dict[str(
            found_history[x])].plot_simulation()
        line_plot_dict[str(found_history[x])].figure.savefig(
            f'{str(found_history[x])}_line_plot')
        x += 1

    simulated_returns_data_dict_nums = {}

    x = 0
    while x < len(mc_dict):
        # Compute summary statistics from the simulated daily returns
        simulated_returns_data_dict[str(found_history[x])] = {
            "mean": list(mc_dict[str(found_history[x])].simulated_return.mean(axis=1)),
            "median": list(mc_dict[str(found_history[x])].simulated_return.median(axis=1)),
            "min": list(mc_dict[str(found_history[x])].simulated_return.min(axis=1)),
            "max": list(mc_dict[str(found_history[x])].simulated_return.max(axis=1))
        }
        # Create a DataFrame with the summary statistics
        simulated_returns_data_dict[str(found_history[x])] = pd.DataFrame(
            simulated_returns_data_dict[str(found_history[x])])
        simulated_returns_data_dict_nums[str(
            found_history[x])] = simulated_returns_data_dict[str(found_history[x])]
        simulated_returns_data_dict[str(
            found_history[x])] = simulated_returns_data_dict[str(found_history[x])].plot()
        #simulated_returns_data_dict[str(found_history[x])] = simulated_returns_data_dict[str(found_history[x])]
        simulated_returns_data_dict[str(found_history[x])].figure.savefig(
            f'{str(found_history[x])}_simulated_returns')

        #testdf = pd.concat([testdf,  pd.DataFrame(simulated_returns_data_dict[str(found_history[x])])], axis=1)

        x += 1

    daily_returns = portfolio_df.pct_change()

    pyscript.write('output', daily_returns)
