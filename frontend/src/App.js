import React from "react";
import {Route, Routes} from "react-router-dom";
import HomePage from "./components/HomePage";

function App() {
    return (
        <main>
            <Routes>
                <Route path="/" element={<HomePage/>}/>
            </Routes>
        </main>
    );
}

export default App;