import { useState } from "react";
import styled from "styled-components";
import { TextField, Grid, Button, Autocomplete } from "@mui/material";
import { Source } from "./App";
type Props = {
  investmentOptions: any;
  addInvestment: (ticker: string, weight: string, source: Source) => void;
};
export const InvestmentSearchField = ({
  investmentOptions,
  addInvestment,
}: Props) => {
  const [value, setValue] = useState<any>("");
  return (
    <InvestmentSearchFormContainer container spacing={2} alignItems="center">
      <Grid item xs={8}>
        <Autocomplete
          value={value}
          autoComplete
          options={investmentOptions}
          defaultValue=""
          getOptionLabel={(option: any) =>
            !option?.contract_ticker_symbol
              ? ""
              : `${option?.contract_ticker_symbol} - ${option?.contract_name}`
          }
          renderInput={(params) => (
            <TextField
              {...params}
              fullWidth
              variant="filled"
              label="What do you want to invest in?"
            />
          )}
          onChange={(_, newValue: any) => {
            setValue(newValue);
          }}
        />
      </Grid>
      <Grid item xs={4}>
        <Button
          variant="contained"
          onClick={() => {
            addInvestment(
              value?.contract_ticker_symbol,
              value?.contract_name,
              value?.source
            );
            setValue({});
          }}
          fullWidth
          style={{ height: "3.5rem" }}
        >
          Add Investment
        </Button>
      </Grid>
    </InvestmentSearchFormContainer>
  );
};

const InvestmentSearchFormContainer = styled(Grid)`
  margin-top: 2rem;
`;
