const moment = require('moment');

const extractImportantData = (text) => {
  const skills = extractSkills(text);
  const experience = extractExperience(text);
  const totalExperience = calculateTotalExperience(experience);
  const languages = extractLanguages(text);
  const education = extractEducation(text);
  return {
    skills,
    experience,
    totalExperience,
    languages,
    education
  };
};

const extractSkills = (text) => {
  const skillRegex = /(python|javascript|sql|java|machine learning|react|css|html|typescript)/gi;
  return text.match(skillRegex) || [];
};

const extractExperience = (text) => {
  const numericExperience = extractNumericExperience(text);
  const dateBasedExperience = extractExperienceFromDates(text);

  return [...numericExperience, ...dateBasedExperience];
};

const extractNumericExperience = (text) => {
  const experienceRegex = /\b(\d+)\s*(years|months)\b/gi;
  const matches = [];
  let match;
  while ((match = experienceRegex.exec(text)) !== null) {
    matches.push({ duration: parseInt(match[1], 10) * (match[2] === 'years' ? 12 : 1) });
  }
  return matches;
};

const extractExperienceFromDates = (text) => {
  const dateRangeRegex =
    /(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*-\s*(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\btill date\b)\s*\d{0,4}/gi;

  const matches = text.match(dateRangeRegex);
  const experiences = [];

  if (matches) {
    matches.forEach((range) => {
      const [start, end] = range.split('-').map((date) => date.trim());
      const startDate = moment(start, ['MMM YYYY', 'MMMM YYYY']);
      const endDate = end.toLowerCase() === 'till date' ? moment().startOf('month') : moment(end, ['MMM YYYY', 'MMMM YYYY']);
      const duration = endDate.diff(startDate, 'months');

      experiences.push({ duration: duration > 0 ? duration : 0 });
    });
  }

  return experiences;
};

const calculateTotalExperience = (experience) => {
  return experience.reduce((total, exp) => total + exp.duration, 0);
};


const extractLanguages = (text) => {
  const languageRegex = /(english|spanish|german|french|italian|chinese|russian|ukrainian)/gi;
  return text.match(languageRegex) || [];
};

const extractEducation = (text) => {
  const fullEducationRegex = /(master'?s|bachelor'?s|master|bachelor)\s+of\s+([\w\s]+)/gi;

  const degrees = [];
  const fields = [];

  let match;
  while ((match = fullEducationRegex.exec(text)) !== null) {
    degrees.push(match[1].toLowerCase());
    fields.push(match[2].toLowerCase());
  }

  return {
    degrees: [...new Set(degrees)],
    fields: [...new Set(fields)]
  };
};

module.exports = { extractImportantData };
