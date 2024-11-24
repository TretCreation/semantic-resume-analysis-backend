const express = require('express');
const { sendToFlask } = require('../utils/httpClient');
const router = express.Router();

router.post('/', async (req, res) => {
  try {
    const { text } = req.body;
    if (!text) {
      return res.status(400).json({ error: 'No text provided' });
    }
    const result = await sendToFlask(text);
    res.status(200).json(result.data);
  } catch (error) {
    res.status(500).json({ message: 'Error during analysis', error: error.message });
  }
});

module.exports = router;