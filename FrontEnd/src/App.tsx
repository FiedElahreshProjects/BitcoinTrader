import React, { useState, ChangeEvent } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { SentimentPieChart } from './components/SentimentPieChart';
import { TechnicalLineChart } from './components/LineComponent';


// Register the required components
ChartJS.register(ArcElement, Tooltip, Legend);

const App: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');

  const handleDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(event.target.value);
  };
  
  const handleStartDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setEndDate(event.target.value);
  };

  return (
    <div className="min-h-screen bg-base-100 p-6 grid grid-cols-12 gap-6">
      {/* Sidebar on the left for inputs */}
      <div className="col-span-3 p-4 border rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Select Date for Pie Chart</h2>
        <input
          type="date"
          value={selectedDate}
          onChange={handleDateChange}
          className="block w-full p-2 border rounded mb-6"
        />
        <h2 className="text-xl font-semibold mb-4">Select Date Range for Line Chart</h2>
        <input
          type="date"
          value={startDate}
          onChange={handleStartDateChange}
          className="block w-full p-2 border rounded mb-4"
        />
        <input
          type="date"
          value={endDate}
          onChange={handleEndDateChange}
          className="block w-full p-2 border rounded"
        />
      </div>

      {/* Line graph in the middle */}
      <div className="col-span-6 flex justify-center items-center">
        {startDate && endDate && <TechnicalLineChart startDate={startDate} endDate={endDate} />}
      </div>

      {/* Empty Div for Shadow Box */}
      <div className="col-span-3 flex justify-center items-center">
        <div className="w-4/5 h-40 border-2 border-gray-300 rounded-lg shadow-lg flex justify-center items-center mb-4">
          <p>Placeholder for Additional Info</p>
        </div>
      </div>

      {/* Pie graph on the top right */}
      <div className="col-span-3 flex justify-center items-start">
        {selectedDate && (
          <div className="w-full max-w-sm">
            <SentimentPieChart selectedDate={selectedDate} />
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
