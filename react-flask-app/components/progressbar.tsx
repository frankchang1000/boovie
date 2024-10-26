import React, { useState } from 'react';
import { useInterval } from '@mantine/hooks';
//import { Button, Progress, useMantineTheme, rgba } from '@mantine/core';
import classes from '../css/progressbar.module.css';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
//import { ChakraProvider, Progress } from '@chakra-ui/react';
//import { Button, Progress } from 'semantic-ui-react'

export default function ProgressBarComponent() {
    return (
        <Box sx={{ width: '100%', height: "50px" }}>
            <LinearProgress variant="indeterminate" sx={{
                    height: '10px', // Customize the height
                    backgroundColor: '#82e6b9',
                    '& .MuiLinearProgress-bar': {
                        backgroundColor: '#3ecf8e', // Change this to your desired color
                    },
                }}/>
        </Box>
    );
}
