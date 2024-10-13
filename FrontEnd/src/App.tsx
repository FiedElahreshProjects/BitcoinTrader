import React, { useEffect, useState, ChangeEvent } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import axios from 'axios';

// Register the required components
ChartJS.register(ArcElement, Tooltip, Legend);

interface SentimentData {
  positive_score: number;
  neutral_score: number;
  negative_score: number;
}

interface ChartData {
  labels: string[];
  datasets: {
    data: number[];
    backgroundColor: string[];
  }[];
}


const SentimentPieChart: React.FC<{ selectedDate: string }> = ({ selectedDate }) => {
  const [chartData, setChartData] = useState<ChartData>({
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        data: [0, 0, 0], // Initial values
        backgroundColor: ['#4CAF50', '#FFC107', '#F44336'], // Colors for the pie chart
      },
    ],
  });

  //create an async function
  const getDate = async () =>{
    if(selectedDate){
      try{
        const { data } = await axios.post<SentimentData>(`http://localhost:8000/daily-sentiment-by-date/`, {date: selectedDate})
        console.log(data)

        setChartData({
          labels: ['Positive', 'Neutral', 'Negative'],
          datasets: [
            {
              data: [data.positive_score, data.neutral_score, data.negative_score],
              backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
            },
          ],
        });
      }catch(error){
        console.error('Error fetching sentiment data:', error);
      }
    }
  }

  useEffect(() => {

    getDate();
  }, [selectedDate]);

  useEffect(() =>{
    console.log(chartData)
  })

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <Pie data={chartData} />
    </div>
  );
};

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
