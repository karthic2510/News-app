import { useState, FormEvent } from 'react';
import axios from 'axios';
import Head from 'next/head';

export default function Home() {
  const [topic, setTopic] = useState('');
  const [header, setHeader] = useState('');
  const [summary, setSummary] = useState('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await axios.post('pages/api/app', { topic });
      setHeader(response.data.header);
      setSummary(response.data.summary);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', textAlign: 'center' }}>
      <Head>
        <title>InformGPT</title>
      </Head>

      <h1 style={{ marginTop: '1in', fontWeight: 'bold' }}>InformGPT</h1>
      <div style={{ marginTop: '2em' }}>
        <p>
          This App is an AI-built, AI-powered app that can take any topic you have
          find the latest news articles over the previous 24 hours and summarize
          them into a single 500-word summary.
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        <textarea
          style={{
            display: 'block',
            margin: '2em auto 0',
            width: '50%',
            height: '2em',
          }}
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter a topic"
        ></textarea>
        <button
          type="submit"
          style={{
            display: 'block',
            margin: '2em auto',
            fontWeight: 'bold',
            backgroundColor: '#4285F4',
            color: 'white',
            padding: '0.5em 1em',
            border: 'none',
            borderRadius: '5px',
          }}
        >
          Get summary
        </button>
      </form>

      <div
        style={{
          backgroundColor: 'white',
          color: 'black',
          padding: '2em',
          width: '80%',
          minHeight: '20em',
          boxSizing: 'border-box',
          wordWrap: 'break-word',
          margin: '2em auto',
        }}
      >
        <h2 style={{ textAlign: 'center', fontWeight: 'bold', textDecoration: 'underline' }}>
          {header}
        </h2>
        <br />
        <br />
        <p>{summary}</p>
      </div>
    </div>
  );
}
