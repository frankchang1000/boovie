import React, { useState } from "react";
import { useRef } from 'react';
import { Text, Group, Button, rem, useMantineTheme } from '@mantine/core';
import { Dropzone, MIME_TYPES } from '@mantine/dropzone';
import { IconCloudUpload, IconX, IconDownload } from '@tabler/icons-react';
import classes from '../css/upload.module.css';
import { DisplayPdf } from "./displaypdf.tsx";

export function DropzoneButton() {
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [pdfUrl, setPdfUrl] = useState<string | null>('');
    const theme = useMantineTheme();
    const openRef = useRef<() => void>(null);

    const handleFileUpload = (files: File[]) => {
        console.log(files);
        const file = files[0];
        console.log(file);
        if (file && file.type === 'application/pdf') {
            setPdfFile(file);
            const url = URL.createObjectURL(file)
            setPdfUrl(url);
            console.log("PDF File Uploaded:", file);
        } else {
            alert("Please upload a valid PDF file.");
        }
    };

    return (
        <div className={classes.wrapper}>
            <div>
                <Dropzone
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
                    <Dropzone.Accept>Drop files here</Dropzone.Accept>
                    <Dropzone.Idle>Upload PDF of Book</Dropzone.Idle>
                </Text>
                <Text ta="center" fz="sm" mt="xs" c="dimmed">
                    Drag&apos;n&apos;drop files here to upload. There is no file size limit.
                </Text>
                </div>
            </Dropzone>
            <Button className={classes.control} size="md" radius="xl" onClick={() => openRef.current?.()}>
                Select file
            </Button>
        </div>
        </div>
    );
}