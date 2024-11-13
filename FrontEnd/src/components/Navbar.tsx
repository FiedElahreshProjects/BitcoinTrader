import { SiBitcoinsv, SiEthereum, SiSolana } from "react-icons/si";

const Navbar = () => {
    return (
        <div className="rounded-lg shadow-lg w-screen h-fit bg-[#1A1A1A] p-3">
            <div className="flex items-center flex-row gap-4 justify-between w-full">
                <h1 className="w-fit text-center text-2xl font-[900] text-[#005B41]">
                    MetaTraderV6
                </h1>
                <div className="w-full flex flex-row justify-end">
                    <div className="flex flex-row items-center justify-evenly px-3 gap-4">
                        {/* Bitcoin Icon and Label */}
                        <div className="group relative w-fit h-fit flex items-center hover:text-[#005B41] transition-all">
                            <SiBitcoinsv className="scale-[1.6] transition-transform group-hover:-translate-x-2"/>
                            <span className="ml-2 opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 text-lg font-bold text-[#005B41] overflow-hidden">
                                BTC
                            </span>
                        </div>
                        
                        {/* Ethereum Icon and Label */}
                        <div className="group relative w-fit h-fit flex items-center hover:text-[#005B41] transition-all">
                            <SiEthereum className="scale-[1.6] transition-transform group-hover:-translate-x-2"/>
                            <span className="ml-2 opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 text-lg font-bold text-[#005B41] overflow-hidden">
                                ETH
                            </span>
                        </div>
                        <div className="group relative w-fit h-fit flex items-center hover:text-[#005B41] transition-all">
                            <SiSolana className="scale-[1.6] transition-transform group-hover:-translate-x-2"/>
                            <span className="ml-2 opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 text-lg font-bold text-[#005B41] overflow-hidden">
                                SOL
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Navbar;
