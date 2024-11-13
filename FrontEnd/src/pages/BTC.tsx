import { SentimentPieChart } from '../components/SentimentPieChart';
import { TechnicalLineChart } from '../components/TechnicalLineComponent';
import { TradingDataProvider } from '../context/TradingDataContext';
import { TradingLineChart } from '../components/TradingLineChart';
import { SMALine } from '../components/SMALine';
import TotalPL from '../components/TotalPL';
import { RSILine } from '../components/RSILine';

const BTC = () =>{
    const formatDate = (date: Date): string => {
        return date.toISOString().split('T')[0];
    };
    return (
        <TradingDataProvider>
            <div className="p-6 lg:grid lg:grid-cols-12 lg:grid-rows-4 gap-6 flex flex-col w-ful h-full">
                {/* Sidebar on the left for inputs */}

                {/* Line graph for BTC price */}
                <div className="col-span-8 row-span-2 h-full flex justify-center bg-[#1A1A1A] rounded-xl shadow-lg p-3 items-center">
                    <TechnicalLineChart formatDate={formatDate}/>
                </div>
                {/* Pie graph on the top right */}
                <div className='col-span-4 row-span-4 h-full w-full grid grid-cols-1 grid-rows-3 gap-6'>
                    <div className="flex justify-center items-center bg-[#1A1A1A] rounded-xl p-3 shadow-lg row-span-2 h-full">
                        <SentimentPieChart formatDate={formatDate} />
                    </div>
                    <div className="grid grid-cols-1 grid-rows-2 gap-4 items-center row-span-1">
                        <TotalPL />
                    </div>
                </div>
                
                {/* Line graph for the Trading history */}
                <div className="col-span-8 row-span-2 flex h-full justify-center bg-[#1A1A1A] rounded-xl shadow-lg p-3 items-center">
                    <TradingLineChart formatDate={formatDate} />
                </div>
            </div>
            <div className='p-6 flex flex-col lg:gap-8 gap-4'>
                <div className="flex h-full justify-center items-center bg-[#1A1A1A] rounded-xl shadow-lg p-4">
                    <SMALine formatDate={formatDate}/>
                </div>
                <div className="flex h-full justify-center items-center bg-[#1A1A1A] rounded-xl shadow-lg p-4">
                    <RSILine formatDate={formatDate}/>
                </div>
            </div>
        </TradingDataProvider>
    )
}

export default BTC;