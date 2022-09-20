import axios from "axios";

const axiosConfig = {
}

export const URL = "localhost:3000"
const customAxios = axios.create(
    axiosConfig
)

export default customAxios;