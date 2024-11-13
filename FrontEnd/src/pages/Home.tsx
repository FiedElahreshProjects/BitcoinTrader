import BTC from "./BTC";
import SideBar from "../components/SideBar";
import useIsDesktop from "../hooks/useIsDesktop";
import Navbar from "../components/Navbar";

const Home = () =>{
    const isDesktop = useIsDesktop();

    return (
        <div className="flex lg:flex-row flex-col justify-between gap-2">
            {isDesktop ? <SideBar /> : <Navbar />}
            <div className="lg:w-[80%] w-full overflow-y-scroll lg:h-screen h-[calc(100vh-64px)] hide-scrollbar custom-scrollbar">
                <BTC />
            </div>
        </div>
    );
}

export default Home;