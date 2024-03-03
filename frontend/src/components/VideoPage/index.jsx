import ReactPlayer from 'react-player';
import React from 'react';
import {useEffect, useState} from "react";
import {
    Stack,
    Paper,
    Link,
    Card,
    CardMedia,
    Switch,
    Chip,
    Rating,
    Grid,
    FormControlLabel,
    Checkbox,
    FormGroup,
    Box,
    Button,
    CircularProgress,
    IconButton,
    InputAdornment,
    TextField,
    Typography,
    Divider,
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from "@mui/material";
import axios from 'axios';
import ReactDOM from 'react-dom';
import {useNavigate} from "react-router-dom";
import {SelectChangeEvent} from '@mui/material/Select';

export default function VideoPage() {
    let links = ["url.txt"];
    let navigate = useNavigate();

    let [texts, setTexts] = useState("");

    const navigateOut = () => {
        navigate("/audio")
    };
    useEffect(() => {
        async function main() {
            const files = await Promise.all(
                links.map((link) => fetch(link).then((res) => res.text()))
            );
            setTexts(files);
        }

        main();
        console.log(texts);
    }, [setTexts]);

    console.log(texts)


    return (
        <>
            <div >
                <ReactPlayer
                    url={texts[0]}
                    controls/>
            </div>

            <Button onClick={navigateOut} variant="contained">Ready!</Button>
        </>
    );
}

