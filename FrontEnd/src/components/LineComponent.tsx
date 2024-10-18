import { useState, useEffect } from "react";
import { Line } from 'react-chartjs-2';
import axios from 'axios';


interface TechnicalData {
  date: string;
  closing_price: number;
}

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    fill: boolean;
  }[];
}

export const TechnicalLineChart: React.FC<{ startDate: string; endDate: string }> = ({ startDate, endDate }) => {
  const [chartData, setChartData] = useState<ChartData>({
    labels: [],
    datasets: [
      {
        label: 'Daily Technical Closing Value',
        data: [],
        borderColor: '#28A745',
        backgroundColor: 'rgba(40, 167, 69, 0.2)',
        fill: true,
      },
    ],
  });

  const getTechnicalData = async () =>{
    if(startDate && endDate){
      try{
        const response = await axios.post<TechnicalData[]>(`http://localhost:8000/daily-technical-by-date/`, {date_start: startDate, date_end: endDate})
        console.log(response.data)
        const labels = response.data.map((item) => item.date);
        const data = response.data.map((item) => item.closing_price);
        console.log(data)

        // Set the chart data using the response from the API
        setChartData({
          labels,
          datasets: [
            {
              label: 'Daily Technical Closing Value',
              data,
              borderColor: '#28A745',
              backgroundColor: 'rgba(40, 167, 69, 0.2)',
              fill: true,
            },
          ],
        });
      }catch(error){
        console.log("error fetching data...", error);
      }
    }
  }

  useEffect(() => {
    getTechnicalData();
  }, [startDate, endDate]);

  return (
    <div className="w-full h-full flex items-center justify-center">
      <Line data={chartData} />
    </div>
  );
};
