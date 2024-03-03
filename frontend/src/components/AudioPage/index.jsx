import React, {useState, useRef, useEffect} from 'react';
import axios, {interceptors} from "axios";
import lamejs from 'lamejs';
import {
    Paper,
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


const AudioRecorder = () => {
    const [audioChunks, setAudioChunks] = useState([]);
    const [isRecording, setIsRecording] = useState(false);
    let [transcript, setTranscript] = useState('');
    const [recognition, setRecognition] = useState(null);

    const mediaRecorderRef = useRef(null);

    const startRecording = () => {
        setIsRecording(true);
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new window.SpeechRecognition();

        recognition.lang = 'en-US';
        recognition.interimResults = true;

        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');
            setTranscript(transcript);
            console.log(transcript);
        };

        recognition.start();
        setRecognition(recognition);

    };

    const [keywords, setKeywords] = useState([]);
    const [intersection, setIntersection] = useState([])

    useEffect(() => {
        axios.get('http://localhost:8080/api/keywords')
            .then(response => {
                console.log(response.data);
                setKeywords(response.data);
            })
            .catch(error => {
                console.error('Error fetching keywords:', error);
            });
    }, []);

    if (!keywords) {
        return (
            <>
                <h1>Loading...</h1>
            </>
        );
    }

    Array.prototype.diff = function (arr2) {
        var ret = [];
        for (var i in this) {
            if (arr2.indexOf(this[i]) > -1) {
                ret.push(this[i]);
            }
        }
        return ret;
    };


    const stopRecording = () => {
        setIsRecording(false);
        if (recognition) {
            recognition.stop();
        }
        if (transcript) {
            const transcriptList = transcript.split(" ");
            console.log(transcriptList);

        }


    };

    const handleSaveRecording = async () => {
        const intersection = keywords.filter(element => transcript.includes(element));
        console.log(intersection);

    };

    return (
        <div>
            <Button onClick={startRecording} variant="contained" disabled={isRecording}>
                Start Recording
            </Button>
            <Button onClick={stopRecording} variant="contained" disabled={!isRecording}>
                Stop Recording
            </Button>
            <Button onClick={handleSaveRecording} variant="contained">
                Save Recording
            </Button>
            <p>Transcript: {transcript}</p>
            <p>Matches: {intersection}</p>
        </div>
    );
};

export default AudioRecorder;
