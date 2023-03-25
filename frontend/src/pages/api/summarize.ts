import { VercelRequest, VercelResponse } from '@vercel/node';
import { execSync } from 'child_process';
import path from 'path';

const handler = async (req: VercelRequest, res: VercelResponse) => {
  // Get the topic from the request
  const topic = req.body.topic;

  // Call the summarize.py script with the topic as an argument
  const pythonScriptPath = path.join(__dirname, '..', 'summarize.py');
  const command = `python3 ${pythonScriptPath} "${topic}"`;
  try {
    const result = execSync(command, { encoding: 'utf-8' });
    const jsonResponse = JSON.parse(result);
    res.status(200).json(jsonResponse);
  } catch (error) {
    console.error('Error executing summarize.py:', error);
    res.status(500).json({ error: 'Failed to summarize the topic' });
  }
};

export default handler;
