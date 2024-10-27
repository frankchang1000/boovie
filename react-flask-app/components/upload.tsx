import React, { useState, useRef, useEffect } from "react";
import { Text, Group, Button, rem, useMantineTheme } from "@mantine/core";
import { Dropzone, MIME_TYPES } from "@mantine/dropzone";
import { IconCloudUpload, IconDownload } from "@tabler/icons-react";
import classes from "../css/upload.module.css";
import AnimatedText from "./AnimatedText";
import VideoPlayer from "./videoplayer.tsx";
import "../src/App.css";

export function DropzoneButton() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>("");
  const [clearPage, setClearPage] = useState(false);
  const [showVideo, setShowVideo] = useState(false); // State to control video display
  const [uploadStatus, setUploadStatus] = useState<string>("Upload PDF of Book");
  const [filePath, setFilePath] = useState<string | null>(null); // State to store the file path from the server
  const theme = useMantineTheme();
  const openRef = useRef<() => void>(null);
  const [algorithmState, setAlgorithmState] = useState<string>("Reading file...")

  const handleFileUpload = (files: File[]) => {
    const file = files[0];
    if (file && file.type === "application/pdf") {
      setPdfFile(file);
      const url = URL.createObjectURL(file);
      setPdfUrl(url);
      console.log("PDF File Uploaded:", file);
      setUploadStatus("Book Uploaded");
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

  const checkProcessingStatus = async (taskId: string) => {
    try {
      const response = await fetch(`http://localhost:5000/status/${taskId}`);
      const data = await response.json();
      setAlgorithmState(data.status); // Update the algorithm state based on the response
    } catch (error) {
      console.error("Error fetching status:", error);
    }
  };

  const uploadToBackend = async () => {
    if (!pdfFile) {
      alert("No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const response = await fetch("http://localhost:5000/upload_pdf", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        console.log("File uploaded successfully:", data.message);
        setFilePath(data.task_id);
        return data; // Assuming task_id is used to identify the uploaded file
        
      } else {
        console.error("Upload failed:", data.error);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const wipePage = async () => {
    setClearPage(true);
    const response = await uploadToBackend(); // Wait for the upload to complete
    const taskId = response.task_id; // Get the task ID from the response
  
    // Polling for status updates
    const intervalId = setInterval(() => {
      checkProcessingStatus(taskId);
    }, 2000); // Check every 2 seconds
  
    setShowVideo(true);
  
    // Clear the interval when the processing is complete
    const checkCompletion = async () => {
      const response = await fetch(`http://localhost:5000/status/${taskId}`);
      const data = await response.json();
      if (data.status === 'completed' || data.status.startsWith('error:')) {
        clearInterval(intervalId);
      }
    };
  
    // Check completion status every 2 seconds
    const completionIntervalId = setInterval(checkCompletion, 2000);
  };

  const undoWipe = () => {
    setClearPage(false);
    setShowVideo(false); // Reset video state when undoing
    setPdfFile(null);
    setPdfUrl(null);
    setUploadStatus("Upload PDF of Book");
  };

  return (
    <div className={classes.wrapper}>
      {!clearPage ? (
        <div>
          <Dropzone
            openRef={openRef}
            onDrop={handleFileUpload}
            className={classes.dropzone}
            radius="md"
            accept={[MIME_TYPES.pdf]}
            maxSize={30 * 1024 ** 2}
            style={{color:'var(--background-color)'}}
          >
            <div style={{ pointerEvents: "none" }}>
              <Group justify="center">
                <Dropzone.Accept>
                  <IconDownload
                    style={{ width: rem(50), height: rem(50) }}
                    color={theme.colors.blue[6]}
                    stroke={1.5}
                  />
                </Dropzone.Accept>
                <Dropzone.Idle>
                  <IconCloudUpload
                    style={{ width: rem(50), height: rem(50) }}
                    stroke={1.5}
                  />
                </Dropzone.Idle>
              </Group>

              <Text ta="center" fw={700} fz="lg" mt="xl" style={{ color:'var(--background-color)' }}>
                <Dropzone.Accept>{uploadStatus}</Dropzone.Accept>
                <Dropzone.Idle>{uploadStatus}</Dropzone.Idle>
              </Text>
              <Text ta="center" fz="sm" mt="xs" c="dimmed">
                Drag&apos;n&apos;drop files here to upload. There is no file
                size limit.
              </Text>
            </div>
          </Dropzone>
          {pdfFile && (
            <Button size="md" radius="xl" color="#3ecf8e" onClick={wipePage}>
              Generate
            </Button>
          )}
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {!showVideo ? (
            <AnimatedText phrase={algorithmState[0]}/>
          ) : (
            <>
              {showVideo && filePath && ( // Use filePath state to pass to VideoPlayer
                <VideoPlayer filePath={`../data/${filePath}_captioned_trailer.mp4`} />
              )}
              <Button size="md" radius="xl" color="#3ecf8e" onClick={undoWipe}>
                Generate Another
              </Button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
