import { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";
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

const API_URL = import.meta.env.VITE_REACT_APP_API_URL;

export const SentimentPieChart: React.FC<{ formatDate: (date:Date) => string}> = ({ formatDate }) => {
    const [selectedDate, setSelectedDate] = useState<string>('');
    const [chartData, setChartData] = useState<ChartData>({
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [
        {
          data: [0, 0, 0], // Initial values
          backgroundColor: ['#28A745', '#A9A9A9', '#1A1A1A'], // Colors for the pie chart
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
            const { data } = await axios.post<SentimentData>(`${API_URL}/daily-sentiment-by-date/`, {date: selectedDate})
    
            setChartData({
              labels: ['Positive', 'Neutral', 'Negative'],
              datasets: [
                {
                  data: [data.positive_score, data.neutral_score, data.negative_score],
                  backgroundColor: ['#005B41', '#A9A9A9', '#1A1A1A'],
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

      const handleDateChange = (event: ChangeEvent<HTMLInputElement>) => {
          setSelectedDate(event.target.value);
      };
      // Calculate recent dates on initial load
      useEffect(() => {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1); // Subtract 1 day
        setSelectedDate(formatDate(yesterday));
    }, []);
  
    useEffect(() => {
      getDate();
    }, [selectedDate]);
  
    return (
      <div className="w-full h-full flex flex-col items-center justify-center">
        <div className="flex flex-col gap-1 justify-center w-full items-center">
          <h2 className="text-gray-300 text-xl xl:text-2xl font-bold mb-1">BTC Sentiment</h2>
          <input
          type="date"
          value={selectedDate}
          onChange={handleDateChange}
          className="w-fit p-2 rounded mb-6"
          />
        </div>
        {error ? (
          <p className="text-[#E53935]">{error}</p>
        ) : (
          <div className="flex items-center justify-center w-full h-full max-h-[280px]"> {/* Centering Container */}
            <Pie data={chartData} options={options}/>
          </div>
        )}
      </div>

    );
  };