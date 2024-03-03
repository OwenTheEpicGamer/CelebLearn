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


export default function HomePage() {
    let navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState()
    const [response, setResponse] = useState()
    const [character, setCharacter] = useState('');

    const handleFileChange = (event) => {
        if (event.target.files && event.target.files.length > 0) {
            console.log(event.target.files[0]);

            setSelectedFile(event.target.files[0]);
        }
    };

    // const handleSelectCharacter = (event) => {
    //     setCharacter(event.target.value);
    //     console.log(character);
    // };

    const handleSelectCharacter = (event) => {
        setCharacter(event.target.value);
    };
    console.log(character);


    const handleUpload = () => {
        if (!selectedFile) {
            console.error('No file selected');
            return;
        }

        if (!character) {
            console.error('No character selected');
            return;
        }


        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('character', character);
        console.log(formData);


        axios.post('http://localhost:8080/api/upload', formData)
            .then(response => {
                console.log(response);
                console.log('File uploaded successfully');
                setResponse(response);
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
    };

    // if (response.data.message) {
    //     navigate('/video')
    // }

    return (
        <>
            <Box className={'flex flex-row'}>
                <Box className={"w=1/2"}>
                    <Box className={'flex flex-col gap-10'}>
                        <title>
                            CELEB-LEARN
                        </title>
                        <p>
                            Want to learn through funny AI generated deepfakes of celebrities?
                        </p>
                        <FormControl fullWidth>

                            <input type="file" onChange={handleFileChange}/>


                            <InputLabel id="demo-simple-select-label">Age</InputLabel>
                            <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={character}
                                label="Age"
                                onChange={handleSelectCharacter}
                            >
                                <MenuItem value={"walter"}>Walter White</MenuItem>
                                <MenuItem value={"obama"}>Obama</MenuItem>
                                <MenuItem value={"trump"}>Trump</MenuItem>
                                <MenuItem value={"biden"}>Biden</MenuItem>

                            </Select>
                            <Button onClick={handleUpload} variant="contained">Upload</Button>

                        </FormControl>


                    </Box>
                </Box>
                <Box className={'w-1/2'}>

                </Box>
            </Box>
        </>
    );
}