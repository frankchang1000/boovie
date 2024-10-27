import React from "react";
import { LuSparkle } from "react-icons/lu"; // Import the LuSparkle icon

interface AnimatedTextProps {
  phrase: string; // Define the prop type
}

const AnimatedText: React.FC<AnimatedTextProps> = ({ phrase }) => {
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
      <div style={{ fontSize: "1.0rem", color: "white" }}>{phrase}</div>
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
