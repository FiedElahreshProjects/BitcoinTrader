import { useState, useEffect } from "react";
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
    }[];
  }

export const SentimentPieChart: React.FC<{ selectedDate: string }> = ({ selectedDate }) => {
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