const path = require('path');
const { loadDataset } = require('../utils/ratingUtils');
const { calculateRating } = require('../utils/ratingUtils');

const filterCandidatesWithRating = async (req, res) => {
  try {
    const datasetPath = path.join(__dirname, '../dataset/data.csv');
    const dataset = await loadDataset(datasetPath);
    const criteria = req.body.criteria;

    if (!criteria || !Array.isArray(criteria) || criteria.length === 0) {
      return res.status(400).json({ message: 'Invalid criteria format. Please provide an array of criteria.' });
    }

    const candidatesWithRating = dataset.map((candidate) => {
      const rating = calculateRating(candidate, criteria);
      return {
        Rating: rating,
        Category: candidate.Category,
        Resume: candidate.Resume,
      };
    });

    const sortedCandidates = candidatesWithRating.sort((a, b) => b.Rating - a.Rating);

    res.status(200).json({
      message: 'Candidates filtered successfully with ratings.',
      candidates: sortedCandidates,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'An error occurred while filtering candidates.', error: error.message });
  }
};

module.exports = {
  filterCandidatesWithRating,
};
