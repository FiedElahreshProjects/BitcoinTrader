import { useState, useEffect, ChangeEvent } from "react";
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import { useTradingData } from "../context/TradingDataContext";

type TechnicalData = {
  date: string;
  closing_price: number;
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

export const TechnicalLineChart: React.FC<{ formatDate: (date: Date) => string }> = ({ formatDate }) => {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const { tradeData } = useTradingData();
  console.log(tradeData);
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
        const data = sortedData.map((item) => item.closing_price);

        setChartData({
          labels,
          datasets: [
            {
              label: 'Daily Technical Closing Value',
              data,
              borderColor: '#005B41',
              backgroundColor: 'rgba(40, 167, 69, 0.2)',
              fill: true,
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
    const twoWeeksAgo = new Date(today);
    twoWeeksAgo.setDate(today.getDate() - 14);
    setEndDate(formatDate(today));
    setStartDate(formatDate(twoWeeksAgo));
  }, []);

  const calculateMonthDifference = (start: string, end: string) => {
    const startDt = new Date(start);
    const endDt = new Date(end);
    const yearDiff = endDt.getFullYear() - startDt.getFullYear();
    const monthDiff = endDt.getMonth() - startDt.getMonth();
    return yearDiff * 12 + monthDiff;
  };

  const isOverSixMonths = calculateMonthDifference(startDate, endDate) > 6;

  return (
    <div className="w-full h-full flex md:flex-row flex-col md:min-h-[0px] min-h-[300px] items-center justify-center gap-6">
      <div className="flex flex-col md:items-start items-center gap-1 md:w-[29%] w-full">
        <h2 className="text-gray-300 text-xl font-[900]">BTC Closing Price</h2>
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
            interaction: {
              mode: isOverSixMonths ? undefined : 'nearest',
              intersect: !isOverSixMonths,
            },
            plugins: {
              tooltip: {
                enabled: !isOverSixMonths,
              },
            },
            elements: {
              point: {
                radius: isOverSixMonths ? 0 : 3, // Set radius to 0 if range > 6 months, else 3
              },
            },
          }}
        />
      </div>
    </div>
  );
};
