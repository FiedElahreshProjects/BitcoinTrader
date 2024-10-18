import { useState, useEffect } from "react";
import axios, { AxiosError } from "axios";
import { Pie } from 'react-chartjs-2';

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
    borderColor: string;
    borderWidth: number;
  }[];
}

export const SentimentPieChart: React.FC<{ selectedDate: string }> = ({ selectedDate }) => {
    const [chartData, setChartData] = useState<ChartData>({
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [
        {
          data: [0, 0, 0], // Initial values
          backgroundColor: ['#28A745', '#A9A9A9', '#000000'], // Colors for the pie chart
          borderColor: '#1C2833', // Darker outline to match the background
          borderWidth: 2, 
        },
      ],
    });
    
    const [error, setError] = useState<string | null>(null);

    const options = {
      plugins: {
        legend: {
          labels: {
            color: '#FFFFFF', // Set the legend text color to white
          },
        },
      },
    };
  
    //create an async function
    const getDate = async () =>{
      if(selectedDate){
        try{
          const { data } = await axios.post<SentimentData>(`http://localhost:8000/daily-sentiment-by-date/`, {date: selectedDate})
  
          setChartData({
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [
              {
                data: [data.positive_score, data.neutral_score, data.negative_score],
                backgroundColor: ['#28A745', '#A9A9A9', '#000000'],
                borderColor: '#1C2833', // Darker outline to match the background
                borderWidth: 2, 
              },
            ],
          });
          setError(null);
        }catch(error){
          // Check if the error is an AxiosError and if it has a response with a status code
          if (axios.isAxiosError(error)) {
            if (error.response && error.response.status === 404) {
              setError("Data unavailable");
            } else {
              setError("An error occurred");
            }
          }
        }
      }
    }
  
    useEffect(() => {
      getDate();
    }, [selectedDate]);
  
    return (
      <div className="w-full h-full flex items-center justify-center">
        {error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <Pie data={chartData} options={options} />
        )}
      </div>
    );
  };