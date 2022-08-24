import "./App.scss";
import { useState } from "react";
import { Typography, CircularProgress, Alert, Grid } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { getCovalentTokens } from "./requests/requests";
import { AxiosError } from "axios";
import ms from "time-to-ms";
import { InvestmentSearchField } from "./InvestmentSearchField";
import { Container } from "@mui/system";

export type Source = "alpaca" | "covalent";

type Investment = {
  alpaca: {
    [key: string]: string;
  };
  covalent: {
    [key: string]: string;
  };
};

function App() {
  const { data, isLoading, isError, error } = useQuery<any, AxiosError>(
    ["covalent-api"],
    () => getCovalentTokens,
    { staleTime: ms("1h") }
  );
  const [selectedInvestments, setSelectedInvestments] = useState<Investment>({
    alpaca: {},
    covalent: {},
  });

  const { items: covalentTokens } = data?.data?.data || {};

  const addInvestment = (ticker: string, weight: string, source: Source) => {
    setSelectedInvestments({
      ...selectedInvestments,
      [source]: {
        ...selectedInvestments[source],
        [ticker]: weight,
      },
    });
  };

  const normalizedInvestments = covalentTokens
    ?.sort((a: any, b: any) =>
      a?.contract_ticker_symbol?.toLowerCase() >
      b?.contract_ticker_symbol?.toLowerCase()
        ? 1
        : -1
    )
    .map((token: any) => {
      return { ...token, source: "covalent" };
    });

  return (
    <div className="App">
      {isLoading && <CircularProgress />}
      {isError && <Alert severity="error">{error?.message}</Alert>}
      <header className="App-header">
        <Typography variant="h3">
          Welcome to the The LTC Portfolio Optimizer
        </Typography>

        <Grid
          container
          justifyContent="center"
          spacing={12}
          alignItems="flex-start"
        >
          <Grid item xs={4}>
            <Grid container justifyContent="space-between">
              {covalentTokens?.length > 0 && (
                <InvestmentSearchField
                  investmentOptions={normalizedInvestments}
                  addInvestment={addInvestment}
                />
              )}
            </Grid>
          </Grid>
          <Grid item xs={2}>
            <Grid
              container
              justifyContent="flex-start"
              style={{ paddingTop: "3rem" }}
            >
              <Typography variant="h4">Selected Investments</Typography>
              <Grid
                container
                direction="column"
                alignItems="flex-start"
                justifyContent="flex-start"
              >
                {Object.keys(selectedInvestments?.covalent)?.length > 0 ? (
                  Object.keys(selectedInvestments?.covalent)?.map(
                    (key, index) => {
                      return (
                        <Typography key={index} variant="body1">
                          {key} - {selectedInvestments?.covalent[key]}
                        </Typography>
                      );
                    }
                  )
                ) : (
                  <Typography variant="body1">
                    No investments selected
                  </Typography>
                )}
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </header>
    </div>
  );
}

export default App;
