import BTC from "./BTC";
import SideBar from "../components/SideBar";

const Home = () =>{
    return (
        <div className="flex flex-row justify-between gap-2">
            <SideBar />
            <div className="w-[80%] overflow-y-scroll h-screen hide-scrollbar custom-scrollbar">
                <BTC />
            </div>
        </div>
    );
}

export default Home;