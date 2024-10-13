import React, { useState, ChangeEvent } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { SentimentPieChart } from './components/SentimentPieChart';


// Register the required components
ChartJS.register(ArcElement, Tooltip, Legend);

const App: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>('');

  const handleDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(event.target.value);
  };

  return (
    <div className="min-h-screen bg-base-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-8">Sentiment Dashboard</h1>
      <div className="max-w-lg mx-auto">
        <input
          type="date"
          value={selectedDate}
          onChange={handleDateChange}
          className="block w-full p-2 border rounded mb-4"
        />
        {selectedDate && <SentimentPieChart selectedDate={selectedDate} />}
      </div>
    </div>
  );
};

export default App;
