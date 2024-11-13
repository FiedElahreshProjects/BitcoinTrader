import { useTradingData } from "../context/TradingDataContext";

const TotalPL = () => {
    const { tradeData } = useTradingData();

    // Calculate total P/L and current capital based on the latest trade data
    const latestTrade = tradeData[tradeData.length - 1];
    const totalPL = latestTrade ? latestTrade.cumulative_profit_loss : 0;
    const currentCapital = latestTrade ? latestTrade.capital : 0;
    const colour = totalPL >= 0 ? '#005B41' : '#E53935'

    return (
        <>
            <div className="bg-[#1A1A1A] w-full h-full rounded-xl shadow-lg flex items-center justify-between text-white p-4">
                <h2 className="text-lg xl:text-xl font-bold">Total P/L:</h2>
                <p className={`text-xl xl:text-2xl text-[${colour}]`}>{totalPL.toFixed(2)}</p>
            </div>
            <div className="bg-[#1A1A1A] w-full h-full rounded-xl shadow-lg flex items-center justify-between text-white p-4">
                <h2 className="text-lg xl:text-xl font-bold">Capital:</h2>
                <p className="text-xl xl:text-2xl">{currentCapital.toFixed(2)}</p>
            </div>
       </>
    );
}

export default TotalPL;