import "./App.scss";
import {
  TextField,
  Grid,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Autocomplete,
} from "@mui/material";
import styled from "styled-components";
import { useQuery } from "@tanstack/react-query";
import { getCovalentTokens } from "./requests/requests";
import { AxiosError } from "axios";
import ms from "time-to-ms";

function App() {
  const { data, isLoading, isError, error } = useQuery<any, AxiosError>(
    ["covalent-api"],
    () => getCovalentTokens,
    { staleTime: ms("1h") }
  );

  const { items: covalentTokens } = data?.data?.data || {};

  return (
    <div className="App">
      {isLoading && <CircularProgress />}
      {isError && <Alert severity="error">{error?.message}</Alert>}
      <header className="App-header">
        <Typography variant="h3">
          Welcome to the The LTC Portfolio Optimizer
        </Typography>
        <TextFieldContainer container>
          <Grid item xs={8}>
            <Autocomplete
              autoComplete
              options={covalentTokens?.map(
                (option: any) =>
                  `${option?.contract_ticker_symbol} - ${option.contract_name}`
              )}
              renderInput={(params) => (
                <TextField
                  {...params}
                  fullWidth
                  variant="filled"
                  label="What do you want to invest in?"
                />
              )}
            />
          </Grid>
          <Grid item xs={4}>
            <Button variant="contained">Add Investment</Button>
          </Grid>
        </TextFieldContainer>
      </header>
    </div>
  );
}

export default App;

const TextFieldContainer = styled(Grid)`
  max-width: 30%;
  margin-top: 2rem;
`;
