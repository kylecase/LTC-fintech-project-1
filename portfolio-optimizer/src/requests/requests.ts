import axios from "axios";
import { API } from "../constants";

export const getCovalentTokens = axios.get(API.COVALENT_URL);
