const express = require('express');
const analyzeRoute = require('./routes/analyzeRoute');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use('/api/analyze', analyzeRoute);

app.listen(port, () => {
  console.log(`Express server running on port ${port}`);
});
