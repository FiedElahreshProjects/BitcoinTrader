import { SiBitcoinsv, SiEthereum } from "react-icons/si";

const SideBar = () =>{
    return (
    <div className="rounded-lg shadow-lg w-[25%] h-screen bg-[#1A1A1A]">
        <div className='flex items-center flex-col gap-3 justify-center w-full mt-3'>
            <h1 className="p-3 w-full text-center text-3xl font-[900] mt-6 text-[#005B41]">
                MetaTrader V6
            </h1>
            <div className='w-full flex flex-col justify-center'>
                <div className='h-16 flex flex-row items-center justify-between px-3 bg-[#121212] hover:text-[#005B41]'>
                    <SiBitcoinsv className='scale-[1.6] ml-2'/>
                    <p className='text-xl font-bold'>
                        Bitcoin
                    </p>
                </div>
                <div className='h-16 flex flex-row items-center justify-between px-3 hover:text-[#005B41]'>
                    <SiEthereum className='scale-[1.6] ml-2 transition-all'/>
                    <p className='text-xl font-bold'>
                        Ethereum
                    </p>
                </div>
            </div>
        </div>
    </div>
    )
}

export default SideBar;