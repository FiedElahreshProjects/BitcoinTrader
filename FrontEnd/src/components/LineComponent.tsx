import { useState, useEffect } from "react";
import { Line } from 'react-chartjs-2';
import axios from 'axios';


interface TechnicalData {
  date: string;
  closing_value: number;
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

useEffect(() => {
    if (startDate && endDate) {
      // Fetch data from the FastAPI backend for the given date range
      axios
        .get<TechnicalData[]>(`http://localhost:8000/daily-technical-by-date/`, {
          params: {
            start_date: startDate,
            end_date: endDate,
          },
        })

        .then((response) => {
          const labels = response.data.map((item) => item.date);
          const data = response.data.map((item) => item.closing_value);

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
        })
        
        .catch((error) => {
          console.error('Error fetching technical data:', error);
        });
    }
  }, [startDate, endDate]);

  return (
    <div style={{ width: '80%', height: '500px', margin: '0 auto' }}>
      <Line data={chartData} />
    </div>
  );
};
