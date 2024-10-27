import React, { useState } from 'react';
import ReactPlayer from 'react-player';
import { Player } from 'video-react';
import "node_modules/video-react/dist/video-react.css";
import classes from "../css/videoplayer.module.css";

/*
export default function() {
    return (
        <div className={classes.videoplayercontainer}>
            <Player
                playsInline
                className={classes.videoplayer}
                poster="../results/hatchet.jpg"
                src="../results/ding.mp4"
            />
        </div>
    );
}
*/

export default function VideoPlayer() {
    const [videoFilePath, setVideoFilePath] = useState<string | null>(null);
    const handleVideoUpload = (event) => {
        setVideoFilePath(URL.createObjectURL(event.target.files[0]));
    };

    return (
        <ReactPlayer
            url={videoFilePath || ''}
            width=  "100%" 
            height= "auto" 
            controls
        />
    );
}
