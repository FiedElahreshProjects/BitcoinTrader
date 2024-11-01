import BTC from "./BTC";
import SideBar from "../components/SideBar";

const Home = () =>{
    return (
        <div className='flex flex-row gap-2'>
            <SideBar />
            <BTC />
        </div>
    );
}

export default Home;