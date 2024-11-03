import { useState, useEffect } from "react";
import { Line } from 'react-chartjs-2';
import { useTradingData } from "../context/TradingDataContext";

export const TradingLineChart: React.FC<{ formatDate: (date: Date) => string }> = ({ formatDate }) => {
  const { tradeData } = useTradingData();

  const latestCapital = tradeData.length > 0 ? tradeData[tradeData.length - 1].capital : 0;
  const averageBuyPrice = tradeData.length > 0 ? tradeData[tradeData.length - 1].avg_buy_price : 0;

  // Find the most recent sell trade to get the last sell profit/loss
  const lastSellTrade = tradeData.slice().reverse().find(trade => trade.action === 'sell');
  const lastTradeProfitLoss = lastSellTrade ? lastSellTrade.trade_profit_loss : 0;

  // Calculate cumulative profit/loss across all trades
  const cumulativeProfitLoss = tradeData.reduce((acc, trade) => acc + trade.trade_profit_loss, 0);

  const [chartData, setChartData] = useState({
    labels: tradeData.map((trade) => formatDate(new Date(trade.decision_date))),
    datasets: [
      {
        label: 'Trade History',
        data: tradeData.map((trade) => trade.price),
        borderColor: cumulativeProfitLoss < 0 ? '#E53935' : '#005B41',  // Red if cumulative P/L is negative, green otherwise
        backgroundColor: cumulativeProfitLoss < 0 ? 'rgba(229, 57, 53, 0.2)' : 'rgba(40, 167, 69, 0.2)',  // Red background for negative P/L
        fill: true,
      },
    ],
  });

  const options = {
    responsive: true,
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context: any) {
            const trade = tradeData[context.dataIndex];
            return `Action: ${trade.action}, Trade P/L: ${trade.trade_profit_loss}, Price: ${trade.price}, Quantity: ${trade.quantity}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Price',
        },
      },
    },
  };

  useEffect(() => {
    setChartData({
      labels: tradeData.map((trade) => formatDate(new Date(trade.decision_date))),
      datasets: [
        {
          label: 'Trade History',
          data: tradeData.map((trade) => trade.price),
          borderColor: cumulativeProfitLoss < 0 ? '#E53935' : '#005B41',  // Update color conditionally based on cumulative P/L
          backgroundColor: cumulativeProfitLoss < 0 ? 'rgba(229, 57, 53, 0.2)' : 'rgba(40, 167, 69, 0.2)',  // Update fill color
          fill: true,
        },
      ],
    });
  }, [tradeData, formatDate, cumulativeProfitLoss]);

  return (
    <div className="w-full h-full flex items-center justify-center gap-6">
      <div className="flex flex-col gap-1 w-[29%]">
        <h2 className="text-gray-300 text-xl font-[900]">All BTC Trades</h2>
        <div className="flex flex-col justify-start text-gray-300 text-sm gap-1"> {/* Default small text */}
          <p><strong className="font-extrabold">Current Capital:</strong> ${latestCapital.toFixed(2)}</p>
          <p><strong className="font-extrabold">Average Buy Price:</strong> ${averageBuyPrice.toFixed(2)}</p>
          <p><strong className="font-extrabold">Last Sell P/L:</strong> ${lastTradeProfitLoss.toFixed(2)}</p>
        </div>
      </div>
      <div className="flex items-center justify-center w-[70%] h-full">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};
