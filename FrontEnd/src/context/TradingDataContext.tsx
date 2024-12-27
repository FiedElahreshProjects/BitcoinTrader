import React, {createContext, useContext, useState, useEffect, ReactNode} from 'react';
import axios from 'axios'

type TradingData = {
    trade_id: number;
    action: string;
    price: number;
    quantity: number;
    avg_buy_price: number;
    trade_profit_loss: number;
    cumulative_profit_loss: number;
    decision_date: Date;
    capital: number;
  };

type TradingDataContextType = {
    tradeData: TradingData[];
    fetchTradeData: () => void;
}

const API_URL = import.meta.env.VITE_REACT_APP_API_URL;

//defines a global container that will hold the shared state and any functions
//provides structure like an empty room that react will use to store the actual data
const TradingDataContext = createContext<TradingDataContextType | undefined>(undefined);

//Responsible for populating the context and making data and functions accessible to any compoennts wrapped in it
//initializes state and supplies context value prop to all components in subtree
export const TradingDataProvider: React.FC<{children: ReactNode}> = ({children}) =>{
    const [tradeData, setTradeData] = useState<TradingData[]>([]);

    const fetchTradeData = async () => {
        try {
          const response = await axios.get<TradingData[]>(`${API_URL}/get_all_trade_data/`);
          const sortedData = response.data.sort((a, b) => {
            const dateA = new Date(a.decision_date);
            const dateB = new Date(b.decision_date);
            return dateA < dateB ? -1 : dateA > dateB ? 1 : 0;
          });
          setTradeData(sortedData);
        } catch (error) {
          console.error("Error fetching trade data:", error);
        }
      };

      useEffect(() =>{
        fetchTradeData();
      }, [])
    
      return (
        <TradingDataContext.Provider value={{ tradeData, fetchTradeData }}>
          {children}
        </TradingDataContext.Provider>
      );
}

//we access global state through the useTradingData hook
export const useTradingData = ()=>{
    const context = useContext(TradingDataContext);
    if(context === undefined){
        throw new Error("useTradingData must be used within a TradingDataProvider");
    }
    return context;
}