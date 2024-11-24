const fs = require('fs');
const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');

const parsePDF = async (filePath) => {
  const fileBuffer = fs.readFileSync(filePath);
  const data = await pdfParse(fileBuffer);
  return data.text;
};

const parseDOCX = async (filePath) => {
  const result = await mammoth.extractRawText({ path: filePath });
  return result.value;
};

const parseResume = async (filePath) => {
  const extension = filePath.split('.').pop().toLowerCase();

  if (extension === 'pdf') {
    return await parsePDF(filePath);
  } else if (extension === 'docx') {
    return await parseDOCX(filePath);
  } else {
    throw new Error('Unsupported file format. Only PDF and DOCX are supported.');
  }
};

module.exports = { parseResume };
