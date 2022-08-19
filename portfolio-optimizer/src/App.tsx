import "./App.scss";
import { TextField, Grid, Typography, Button } from "@mui/material";
import styled from "styled-components";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Typography variant="h3">
          Welcome to the The LTC Portfolio Optimizer
        </Typography>
        <BodyText variant="body1">What would you like to invest in?</BodyText>
        <TextFieldContainer container>
          <Grid item xs={8}>
            <TextField
              fullWidth
              variant="filled"
              label="Enter your first investment"
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
`;

const BodyText = styled(Typography)`
  margin: 1rem;
`;
