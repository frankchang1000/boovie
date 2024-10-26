import "@mantine/core/styles.css";
import { useState, useEffect } from "react";
import "./App.css";
import { createTheme, MantineProvider, Title, Text } from "@mantine/core";
import { DropzoneButton } from "../components/upload";
import { CardsCarousel } from "../components/carousel";
import { ActionToggle } from "../components/themeselector";
import Slider from "../components/slider";

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
        <Title order={1} size="h1" style={{ marginBottom: "2rem" }}>
          Preview Your Next Great Read in an{" "}
          <Text
            component="span"
            inherit
            color="blue"
            style={{ display: "inline" }}
          >
            Immersive Trailer
          </Text>
        </Title>
        <Slider />
        <DropzoneButton />
        {/* Pass the themeMode state and setThemeMode function to ActionToggle */}
        <ActionToggle theme={themeMode} setTheme={setThemeMode} />
      </MantineProvider>
    </>
  );
}

export default App;
