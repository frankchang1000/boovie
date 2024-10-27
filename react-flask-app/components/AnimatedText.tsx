import React, { useEffect, useState } from 'react';

const phrases = ["Reading...", "Generating summaries...", "Generating scripts...", "Generating images...", "Generating video..."];

const AnimatedText: React.FC = () => {
    const [index, setIndex] = useState(0);

    useEffect(() => {
        // Only set interval if not on the last phrase
        if (index < phrases.length - 1) {
            const interval = setInterval(() => {
                setIndex((prevIndex) => prevIndex + 1);
            }, 5000); 

            return () => clearInterval(interval); // Cleanup interval
        }
    }, [index]);

    return (
        <div style={{ textAlign: 'center', fontSize: '1.2rem', color: '#3ecf8e', marginTop: '0.5rem' }}>
            {phrases[index]}
        </div>
    );
};

export default AnimatedText;
