import { useState, useEffect, ChangeEvent } from "react";
import { Line } from 'react-chartjs-2';
import axios from 'axios';

type TechnicalData = {
  date: string;
  sma_7: number;
  sma_21: number;
  rsi: number;
}

type ChartData = {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    fill: boolean;
  }[];
}

export const SMALine: React.FC<{ formatDate: (date: Date) => string }> = ({ formatDate }) => {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [chartData, setChartData] = useState<ChartData>({
    labels: [],
    datasets: [],
  });

  const getTechnicalData = async () => {
    if (startDate && endDate) {
      try {
        const response = await axios.post<TechnicalData[]>(`http://localhost:8000/daily-technical-by-date/`, { date_start: startDate, date_end: endDate });
        const sortedData = response.data.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return dateA < dateB ? -1 : dateA > dateB ? 1 : 0;
        });

        const labels = sortedData.map((item) => item.date);
        const sma7Data = sortedData.map((item) => item.sma_7);
        const sma21Data = sortedData.map((item) => item.sma_21);

        setChartData({
          labels,
          datasets: [
            {
              label: 'SMA 7',
              data: sma7Data,
              borderColor: '#005B41', // Orange for SMA 7
              backgroundColor: 'rgba(255, 165, 0, 0.2)',
              fill: false,
            },
            {
              label: 'SMA 21',
              data: sma21Data,
              borderColor: '#FF0000', // Red for SMA 21
              backgroundColor: 'rgba(255, 0, 0, 0.2)',
              fill: false,
            },
          ],
        });
      } catch (error) {
        console.log("error fetching data...", error);
      }
    }
  }

  const handleStartDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setEndDate(event.target.value);
  };

  useEffect(() => {
    getTechnicalData();
  }, [startDate, endDate]);

  useEffect(() => {
    const today = new Date();
    const sixMonthsAgo = new Date(today);
    sixMonthsAgo.setDate(today.getDate() - 180);
    setEndDate(formatDate(today));
    setStartDate(formatDate(sixMonthsAgo));
  }, []);

  return (
    <div className="w-full h-full flex md:flex-row flex-col md:min-h-[0px] min-h-[300px] items-center justify-center gap-6">
      <div className="flex flex-col md:items-start items-center gap-1 md:w-[29%] w-full">
        <h2 className="text-gray-300 text-xl font-[900]">BTC SMA_7 & SMA_21</h2>
        <h2 className="text-md md:mb-4 mb-2">Select Date Range</h2>
        <div className="flex md:flex-col flex-row md:justify-start md:gap-0 gap-2">
          <input
            type="date"
            value={startDate}
            onChange={handleStartDateChange}
            className="w-full p-2 rounded md:mb-4"
          />
          <input
            type="date"
            value={endDate}
            onChange={handleEndDateChange}
            className="w-full p-2 rounded"
          />
        </div>
      </div>
      <div className="flex items-center justify-center md:w-[70%] w-full h-full">
        <Line
          data={chartData}
          options={{
            elements: {
              point: {
                radius: 0, // Set radius to 0 if range > 6 months, else 3
              },
            },
          }}
        />
      </div>
    </div>
  );
};
