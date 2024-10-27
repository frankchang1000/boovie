import React, { useState } from 'react';
import ReactPlayer from 'react-player';

export default function VideoPlayer({ filePath }) {
  return (
    <div>
      {filePath ? (
        <div
          style={{
            borderRadius: "10px 10px 10px 10px",
            marginBottom: "20px",
            overflow: "hidden",
            padding: "0",
            backgroundColor: "black",
          }}
        >
          <ReactPlayer
            url={filePath}
            width="100%"
            height="100%"
            controls={true}
          />
        </div>
      ) : (
        <p>No video file path provided</p>
      )}
    </div>
  );
}
