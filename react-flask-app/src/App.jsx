import "@mantine/core/styles.css";
import { useState } from "react";
import "./App.css";
import {
  createTheme,
  MantineProvider,
  ColorSchemeProvider,
  Title,
  Text,
} from "@mantine/core";
import { DropzoneButton } from "../components/upload";
import { CardsCarousel } from "../components/carousel";
import { ActionToggle } from "../components/themeselector";
import Slider from "../components/slider";

const theme = createTheme({
  /** Put your mantine theme override here */
});

function App() {
  const [colorScheme, setColorScheme] = useState("light");

  const toggleColorScheme = (value) => {
    const nextColorScheme =
      value || (colorScheme === "dark" ? "light" : "dark");
    setColorScheme(nextColorScheme);
    document.documentElement.setAttribute("data-theme", nextColorScheme);
  };

  return (
    <ColorSchemeProvider
      colorScheme={colorScheme}
      toggleColorScheme={toggleColorScheme}
    >
      <MantineProvider theme={theme} colorScheme={colorScheme}>
        <div className="app-container">
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
          <CardsCarousel />
          <DropzoneButton />
          <ActionToggle />
        </div>
      </MantineProvider>
    </ColorSchemeProvider>
  );
}

export default App;
