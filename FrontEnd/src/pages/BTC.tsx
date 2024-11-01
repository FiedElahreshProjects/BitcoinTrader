import { SentimentPieChart } from '../components/SentimentPieChart';
import { TechnicalLineChart } from '../components/LineComponent';

const BTC = () =>{
    const formatDate = (date: Date): string => {
        return date.toISOString().split('T')[0];
    };
    return (
        <div className="h-[calc(100vh-48px)] p-10 grid grid-cols-12 grid-rows-2 gap-6 w-full">
            {/* Sidebar on the left for inputs */}

            {/* Line graph in the middle */}
            <div className="col-span-8 flex justify-center bg-[#1A1A1A] rounded-xl shadow-lg p-3 items-center">
                <TechnicalLineChart formatDate={formatDate}/>
            </div>


            {/* Pie graph on the top right */}
            <div className="col-span-4 flex justify-center items-center bg-[#1A1A1A] rounded-xl h-fit p-3 shadow-lg">
                <SentimentPieChart formatDate={formatDate} />
            </div>
            {/* Empty Div for Shadow Box */}
            <div className="col-span-3 flex justify-center items-center">
                <div className="w-4/5 h-40 border-2 border-gray-300 rounded-lg shadow-lg flex justify-center items-center mb-4">
                <p>Placeholder for Additional Info</p>
                </div>
            </div>
        </div>
    )
}

export default BTC;