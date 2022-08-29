const express = require("express");
const app = express();
const port = process.env.API_PORT || 8080;
const path = require("path");
const cors = require("cors");

const alpaca = require("./alpaca");

app.get("/api", cors());
app.use("/api/alpaca", alpaca);

if (process.env.NODE_ENV !== "development") {
  app.use(express.static(path.join(__dirname, "../build")));
  app.get("*", (_, res) => {
    res.sendFile(path.join(__dirname, "../build", "index.html"));
  });
}

app.listen(port, () => {
  console.log("Listening on port " + port);
});
