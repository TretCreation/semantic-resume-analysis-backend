const express = require('express');
const { analyzeDatasetWithCriteria } = require('../controllers/candidateController');

const router = express.Router();

router.post('/analyze-dataset', analyzeDatasetWithCriteria);

module.exports = router;
