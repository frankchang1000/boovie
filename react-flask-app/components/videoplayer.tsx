import React, { useState } from 'react';
import ReactPlayer from 'react-player';
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

export default function VideoPlayer({filePath}) {
    return (
        <div>
          {filePath ? (
            <ReactPlayer
              url={filePath}
              width="100%"
              height="100%"
              controls={true}
            />
          ) : (
            <p>No video file path provided</p>
          )}
        </div>
      );
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
