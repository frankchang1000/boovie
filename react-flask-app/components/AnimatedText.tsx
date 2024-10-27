import React, { useEffect, useState } from "react";
import { LuSparkle } from "react-icons/lu"; // Import the LuSparkle icon

const phrases = [
  "Reading...",
  "Generating summaries...",
  "Generating scripts...",
  "Generating images...",
  "Generating video...",
];

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
    <div
      style={{
        display: "flex",
        alignItems: "center",
        textAlign: "center",
        marginTop: "0.5rem",
      }}
    >
      <LuSparkle
        style={{
          fontSize: "2rem",
          color: "#3ecf8e",
          marginRight: "0.5rem",
          animation: "spin 2s linear infinite", // Inline spinning animation
        }}
      />
      <div style={{ fontSize: "1.0rem", color: "white" }}>{phrases[index]}</div>
      <style>{`
                @keyframes spin {
                    from {
                        transform: rotate(0deg);
                    }
                    to {
                        transform: rotate(360deg);
                    }
                }
            `}</style>
    </div>
  );
};

export default AnimatedText;
