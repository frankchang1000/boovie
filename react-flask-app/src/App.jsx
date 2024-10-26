import "@mantine/core/styles.css";
import { useState, useEffect } from "react";
import "./App.css";
import { createTheme, MantineProvider, Title, Text } from "@mantine/core";
import { DropzoneButton } from "../components/upload";
import { ActionToggle } from "../components/themeselector";
import Slider from "../components/slider";
import NavBar from "../components/navbar";

// Define your Mantine theme override
const theme = createTheme({
  /** Put your mantine theme override here */
});

function App() {
  const [themeMode, setThemeMode] = useState("light");

  useEffect(() => {
    // Set the selected theme by applying the data-theme attribute on the body
    document.body.setAttribute("data-theme", themeMode);
  }, [themeMode]);

  return (
    <>
      <MantineProvider theme={theme}>
        <NavBar />
        <div className="titleStyle">
          <h1 className="mainTitle"> Preview Your Next Great Read </h1>
          <h1 className="immersive-trailer"> in an Immersive Trailer</h1>
          <p>
            Upload your own novel or choose from our trending book presets to
            watch a trailer before selecting your next read.
          </p>
        </div>
        <h3 className="trending-header">TRENDING</h3>
        <Slider />
        <DropzoneButton />
      </MantineProvider>
    </>
  );
}

export default App;
