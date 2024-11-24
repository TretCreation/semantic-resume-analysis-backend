const express = require('express');
require('dotenv').config();

const candidateRoutes = require('./routes/candidateRoutes');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Роуты
app.use('/api/candidates', candidateRoutes);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
