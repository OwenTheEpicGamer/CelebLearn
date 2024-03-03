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

const VideoPlayer = ({ url }) => (
    <>
        <div>
            <ReactPlayer
                url={"https://synchlabs-public.s3.amazonaws.com/lip-sync-jobs/a3f47134-d57a-4e60-8dac-3f2bd5236af9/dc67c55d-5320-4c5e-a0a4-6a587fe919a1/result.mp4"}
                controls/>
        </div>

        <Button variant="contained">Ready!</Button>
    </>
);

export default VideoPlayer;