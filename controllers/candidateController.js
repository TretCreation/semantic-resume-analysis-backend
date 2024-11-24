const path = require('path');
const fs = require('fs');
const { parseResume } = require('../utils/resumeParser');
const { calculateRating } = require('../utils/ratingUtils');
const { extractImportantData } = require('../utils/extractUtils');

const analyzeDatasetWithCriteria = async (req, res) => {
  try {
    const resumesDir = path.join(__dirname, '../dataset/resumes');
    const files = fs.readdirSync(resumesDir);
    const criteria = req.body.criteria;

    if (!criteria || !Array.isArray(criteria) || criteria.length === 0) {
      return res.status(400).json({ message: 'Invalid criteria format. Please provide an array of criteria.' });
    }

    const candidates = [];
    for (const file of files) {
      const filePath = path.join(resumesDir, file);
      const resumeText = await parseResume(filePath);
      const extractedData = extractImportantData(resumeText);
      const rating = calculateRating(extractedData, criteria);

      candidates.push({
        FileName: file,
        Rating: rating,
        ExtractedData: extractedData,
      });
    }

    const sortedCandidates = candidates.sort((a, b) => b.Rating - a.Rating);

    res.status(200).json({
      message: 'Resumes analyzed successfully.',
      candidates: sortedCandidates,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'An error occurred while analyzing resumes.', error: error.message });
  }
};

module.exports = { analyzeDatasetWithCriteria };
