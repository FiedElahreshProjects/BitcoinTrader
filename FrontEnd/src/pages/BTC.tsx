import { SentimentPieChart } from '../components/SentimentPieChart';
import { TechnicalLineChart } from '../components/TechnicalLineComponent';
import { TradingDataProvider } from '../context/TradingDataContext';
import { TradingLineChart } from '../components/TradingLineChart';

const BTC = () =>{
    const formatDate = (date: Date): string => {
        return date.toISOString().split('T')[0];
    };
    return (
        <TradingDataProvider>
            <div className="h-screen p-8 grid grid-cols-12 grid-rows-4 gap-6 w-full">
                {/* Sidebar on the left for inputs */}

                {/* Line graph for BTC price */}
                <div className="col-span-8 row-span-2 flex justify-center bg-[#1A1A1A] rounded-xl shadow-lg p-3 items-center">
                    <TechnicalLineChart formatDate={formatDate}/>
                </div>
                {/* Pie graph on the top right */}
                <div className="col-span-4 row-span-3 flex justify-center items-center bg-[#1A1A1A] rounded-xl h-fit p-3 shadow-lg">
                    <SentimentPieChart formatDate={formatDate} />
                </div>
                {/* Line graph for the Trading history */}
                <div className="col-span-8 row-span-2 flex justify-center bg-[#1A1A1A] rounded-xl shadow-lg p-3 items-center">
                    <TradingLineChart formatDate={formatDate} />
                </div>
                <div className="col-span-4 flex justify-center bg-[#1A1A1A] rounded-xl shadow-lg p-3 items-center">
                    
                </div>
            </div>
        </TradingDataProvider>
    )
}

export default BTC;