import React, { useState } from "react";
import { useRef } from 'react';
import { Text, Group, Button, rem, useMantineTheme } from '@mantine/core';
import { Dropzone, MIME_TYPES } from '@mantine/dropzone';
import { IconCloudUpload, IconX, IconDownload } from '@tabler/icons-react';
import classes from '../css/upload.module.css';
import { DisplayPdf } from "./displaypdf.tsx";
import { Progress, Box, ChakraProvider } from '@chakra-ui/react';
import ProgressBarComponent from "./progressbar.tsx";

export function DropzoneButton() {
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [pdfUrl, setPdfUrl] = useState<string | null>('');
    const [clearPage, setClearPage] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<string>('Upload PDF of Book'); // New state for upload status
    const theme = useMantineTheme();
    const openRef = useRef<() => void>(null);

    const handleFileUpload = (files: File[]) => {
        const file = files[0];
        if (file && file.type === 'application/pdf') {
            setPdfFile(file);
            const url = URL.createObjectURL(file);
            setPdfUrl(url);
            console.log("PDF File Uploaded:", file);
            setUploadStatus('Book uploaded'); // Update upload status
        } else {
            alert("Please upload a valid PDF file.");
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
            const response = await fetch("http://localhost:5000/api/upload", {
                method: "POST",
                body: formData,
            });
    
            const data = await response.json();
            if (response.ok) {
                console.log("File uploaded successfully:", data.message);
            } else {
                console.error("Upload failed:", data.error);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };
        
    const wipePage = () => {
        uploadToBackend();
        setClearPage(true);
    }
    
    const undoWipe = () => {
        setClearPage(false);
        setUploadStatus('Upload PDF of Book'); // Reset upload status
    }

    return (
        <div className={classes.wrapper}>
            {!clearPage ? 
            (<div><Dropzone
                openRef={openRef}
                onDrop={handleFileUpload}
                className={classes.dropzone}
                radius="md"
                accept={[MIME_TYPES.pdf]}
                maxSize={30 * 1024 ** 2}
            >
                <div style={{ pointerEvents: 'none' }}>
                    <Group justify="center">
                        <Dropzone.Accept>
                                <IconDownload
                                style={{ width: rem(50), height: rem(50) }}
                                color={theme.colors.blue[6]}
                                stroke={1.5}
                            />
                        </Dropzone.Accept>
                        <Dropzone.Idle>
                            <IconCloudUpload style={{ width: rem(50), height: rem(50) }} stroke={1.5} />
                        </Dropzone.Idle>
                    </Group>

                    <Text ta="center" fw={700} fz="lg" mt="xl">
                        <Dropzone.Accept>{uploadStatus}</Dropzone.Accept> {/* Use uploadStatus here */}
                        <Dropzone.Idle>{uploadStatus}</Dropzone.Idle>
                    </Text>
                    <Text ta="center" fz="sm" mt="xs" c="dimmed">
                        Drag&apos;n&apos;drop files here to upload. There is no file size limit.
                    </Text>
                </div>
            </Dropzone>
            
            <Button size="md" radius="xl" color="#3ecf8e" onClick={wipePage}>
                Upload
            </Button></div>) : (
                <div>
                    <ProgressBarComponent />
                    <Button size="md" radius="xl"  color="#3ecf8e" onClick={undoWipe}>Undo Wipe</Button>
                </div>
            )}
        </div>
    );
}
{/*<Button className={classes.control} size="md" radius="xl" onClick={() => openRef.current?.()}>
                Select Files
            </Button>*/}
