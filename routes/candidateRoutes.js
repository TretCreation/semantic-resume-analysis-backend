const express = require('express');
const { filterCandidatesWithRating } = require('../controllers/candidateController');

const router = express.Router();

router.post('/filter', filterCandidatesWithRating);

module.exports = router;
