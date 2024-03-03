import React, {useState, useRef, useEffect} from 'react';
import axios from "axios";
import lamejs from 'lamejs';

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
        if (audioChunks.length === 0) {
            console.warn('No audio recorded');
            return;
        }

        // Encode audio chunks to MP3
        const mp3Encoder = new lamejs.Mp3Encoder(1, 44100, 128);
        const pcmData = audioChunks.map(chunk => new Int16Array(chunk));
        const mp3Data = mp3Encoder.encodeBuffer(pcmData.flat());

        // Create Blob from encoded MP3 data
        const mp3Blob = new Blob([new Uint8Array(mp3Data)], {type: 'audio/mp3'});

        // Upload MP3 file to backend endpoint
        if (transcript) {

            // try {
            //     const formData = new FormData();
            //     formData.append('audio', mp3Blob, 'recorded_audio.mp3');
            //     await axios.post('http://localhost:8080/api/upload_audio', formData, {
            //         headers: {
            //             'Content-Type': 'multipart/form-data',
            //         },
            //     });
            //     console.log('Recording uploaded successfully');
            // } catch (error) {
            //     console.error('Error uploading recording:', error);
            // }
        }

        // Reset state for next recording
        setAudioChunks([]);
    };

    return (
        <div>
            <button onClick={startRecording} disabled={isRecording}>
                Start Recording
            </button>
            <button onClick={stopRecording} disabled={!isRecording}>
                Stop Recording
            </button>
            <button onClick={handleSaveRecording} disabled={audioChunks.length === 0}>
                Save Recording
            </button>
            <p>Transcript: {transcript}</p>
        </div>
    );
};

export default AudioRecorder;
