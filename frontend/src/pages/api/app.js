import axios from 'axios';

export default async function handler(req, res) {
  const { topic } = req.body;
  try {
    const response = await axios.post('http://127.0.0.1:5000/app/summarize', { topic });
    res.status(200).json(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'An error occurred while fetching the summary.' });
  }
}
