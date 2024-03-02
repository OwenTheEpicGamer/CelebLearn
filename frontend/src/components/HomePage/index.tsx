import * as React from 'react';
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
    Divider
} from "@mui/material";
import axios from 'axios';

export default function HomePage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            console.log(event.target.files[0]);

            setSelectedFile(event.target.files[0]);
        }
    };

    const handleUpload = () => {
        if (!selectedFile) {
            console.error('No file selected');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        axios.post('/api/upload', formData)
            .then(response => {
                console.log('File uploaded successfully');
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
    };

    return (
        <>
            <Box className={'flex flex-row'}>
                <Box className={"w=1/2"}>
                    <Box className={'flex flex-col'}>
                        <title>
                            CELEB-LEARN
                        </title>
                        <p>
                            Want to learn through funny AI generated deepfakes of celebrities?
                        </p>
                        <Button onClick={handleUpload} variant="contained">Upload</Button>
                        <input type="file" onChange={handleFileChange}/>
                    </Box>
                </Box>
                <Box className={'w-1/2'}>

                </Box>
            </Box>
        </>
    );
}