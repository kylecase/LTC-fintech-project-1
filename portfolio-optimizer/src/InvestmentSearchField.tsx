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
  const [weight, setWeight] = useState("");

  const submit = () => {
    addInvestment(value?.contract_ticker_symbol, weight, value?.source);
    setValue({});
    setWeight("");
  };
  return (
    <InvestmentSearchFormContainer
      container
      spacing={2}
      alignItems="center"
      onKeyPress={(e) => {
        if (e.key === "Enter") {
          submit();
        }
      }}
    >
      <Grid item xs={10}>
        <Grid container direction="column" justifyContent="flex-start">
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
          <TextField
            label="Weight"
            variant="filled"
            onChange={(e) => setWeight(e.target.value)}
            value={weight}
          />
        </Grid>
        <Button
          variant="contained"
          onClick={() => submit()}
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
