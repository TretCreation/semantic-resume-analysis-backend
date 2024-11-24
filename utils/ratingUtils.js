const calculateRating = (extractedData, criteria) => {
  let rating = 0;

  criteria.forEach((criterion) => {
    if (criterion.totalExperience && extractedData.totalExperience >= criterion.totalExperience) {
      rating += 1;
    }

    if (criterion.skill && criterion.skill.trim() !== '' && extractedData.skills.includes(criterion.skill.toLowerCase())) {
      rating += 1;
    }

    if (criterion.language && extractedData.languages.includes(criterion.language.toLowerCase())) {
      rating += 1;
    }
  });

  if (extractedData.education && extractedData.education.degrees) {
    extractedData.education.degrees.forEach((degree) => {
      if (degree.includes("master") || degree.includes("bachelor")) {
        rating += 1;
      }
    });
  }

  return rating;
};

module.exports = { calculateRating };
