const fs = require('fs');
const csv = require('csv-parser');

const loadDataset = (datasetPath) => {
  return new Promise((resolve, reject) => {
    const data = [];
    fs.createReadStream(datasetPath)
      .pipe(csv())
      .on('data', (row) => data.push(row))
      .on('end', () => resolve(data))
      .on('error', (err) => reject(err));
  });
};

const calculateRating = (candidate, criteria) => {
  const resume = candidate.Resume ? candidate.Resume.toLowerCase() : '';
  let rating = 0;

  criteria.forEach((criterion) => {
    if (criterion.skill) {
      const skillRegex = new RegExp(`${criterion.skill}.*\\b(\\d+)\\s*(months|years)\\b`, 'i');
      const lessThanOneYearRegex = new RegExp(`${criterion.skill}.*less than 1 year`, 'i');
      const skillMatch = resume.match(skillRegex);
      const lessThanOneYearMatch = resume.match(lessThanOneYearRegex);

      if (skillMatch && parseInt(skillMatch[1], 10) >= criterion.experience) {
        rating += 1;
      } else if (lessThanOneYearMatch && criterion.experience <= 12) {
        rating += 1;
      }
    }

    if (criterion.language) {
      const languageRegex = new RegExp(criterion.language, 'i');
      if (languageRegex.test(resume)) {
        rating += 1;
      }
    }
  });

  return rating;
};

module.exports = {
  loadDataset,
  calculateRating,
};
