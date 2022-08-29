const express = require("express");
const router = express.Router();
const axios = require("axios");
require("dotenv").config();

router.get("/tokens", async (_, res) => {
  try {
    const response = await axios.get(
      "https://api.covalenthq.com/v1/1/xy=k/uniswap_v2/tokens/?quote-currency=USD&format=JSON&page-size=300&key=" +
        process.env.REACT_APP_COVALENT_API_KEY
    );
    return res.json(response.data);
  } catch (e) {
    return res.json({ error: e });
  }
});

router.get("/historical/:contractId", async (req, res) => {
  try {
    const response = await axios.get(
      `https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/1/USD/${req.params.contractId}/?quote-currency=USD&format=JSON&from=2017-08-01&to=2022-08-01&page-number=1&page-size=300&key=${process.env.REACT_APP_COVALENT_API_KEY}`
    );
    return res.json(response.data);
  } catch (e) {
    console.log(e);
    return res.json({ error: e });
  }
});

module.exports = router;
