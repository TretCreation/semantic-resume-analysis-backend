const axios = require('axios');

const sendToFlask = async (text) => {
  const response = await axios.post('http://127.0.0.1:5001/analyze', { text });
  return response;
};

module.exports = { sendToFlask };
