import "@mantine/core/styles.css";
import { useState } from "react";
import "./App.css";
import { createTheme, MantineProvider, Title, Text } from "@mantine/core";
import { DropzoneButton } from "../components/upload";
import { CardsCarousel } from "../components/carousel";
import { ActionToggle } from "../components/themeselector";

import Slider from "../components/slider";

const theme = createTheme({
  /** Put your mantine theme override here */
});

function App() {
  const [count, setCount] = useState(0);

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
        <ActionToggle />
      </MantineProvider>
    </>
  );
}

export default App;
