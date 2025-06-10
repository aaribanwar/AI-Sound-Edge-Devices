// src/components/SoundGraph.jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import '../styles/SoundGraph.css';

const data = [
  { time: '12:00', type: 1 },
  { time: '12:05', type: 3 },
  { time: '12:10', type: 2 },
  { time: '12:15', type: 4 },
  { time: '12:20', type: 1 },
];

const SoundGraph = () => {
  return (
    <div className="card sound-graph">
      <h3>📈 Sound Frequency Over Time</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
          <Line type="monotone" dataKey="type" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SoundGraph;
