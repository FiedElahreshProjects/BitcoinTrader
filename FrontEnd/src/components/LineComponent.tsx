import { useState, useEffect, ChangeEvent } from "react";
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

export const TechnicalLineChart: React.FC<{ formatDate: (date:Date) => string}> = ({ formatDate }) => {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
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
              borderColor: '#005B41',
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
  const handleStartDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event: ChangeEvent<HTMLInputElement>) => {
    setEndDate(event.target.value);
  };

  useEffect(() => {
    getTechnicalData();
  }, [startDate, endDate]);

  useEffect(() =>{
    const today = new Date();
   
    // Set endDate and selectedDate to yesterday
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 2);
    
    // Set startDate to two weeks prior to yesterday
    const twoWeeksAgo = new Date(yesterday);
    twoWeeksAgo.setDate(yesterday.getDate() - 14);
    setEndDate(formatDate(yesterday));
    setStartDate(formatDate(twoWeeksAgo));
  }, [])

  return (
    <div className="w-full h-full flex items-center justify-center gap-6">
      <div className="flex flex-col gap-1 w-full">
          <h2 className="text-gray-300 text-xl font-[900]">BTC Closing Price</h2>
          <div className="flex flex-col justify-start">
            <h2 className="text-md mb-4">Select Date Range</h2>
            <input
            type="date"
            value={startDate}
            onChange={handleStartDateChange}
            className="w-full p-2 rounded mb-4"
            />
            <input
            type="date"
            value={endDate}
            onChange={handleEndDateChange}
            className="w-full p-2 rounded"
            />
          </div>
      </div>
      
      <Line data={chartData} />
    </div>
  );
};
