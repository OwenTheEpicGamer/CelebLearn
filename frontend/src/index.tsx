import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider } from "@mui/material";
import theme from "./context/theme";
import { createRoot } from 'react-dom/client';
const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
                <BrowserRouter>
                    <App />
                </BrowserRouter>
        </ThemeProvider>
    </React.StrictMode>
);