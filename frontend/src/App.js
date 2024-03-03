import React from "react";
import {Route, Routes} from "react-router-dom";
import HomePage from "./components/HomePage";
import VideoPage from "./components/VideoPage";
import AudioPage from "./components/AudioPage";



function App() {
    return (
        <main>
            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/video" element={<VideoPage/>}/>
                <Route path="/audio" element={<AudioPage/>}/>

            </Routes>
        </main>
    );
}

export default App;