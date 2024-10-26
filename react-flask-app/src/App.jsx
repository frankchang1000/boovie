import "@mantine/core/styles.css";
import { useState } from "react";
import "./App.css";
import { createTheme, MantineProvider } from "@mantine/core";
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
        <Slider />
        <CardsCarousel />
        <DropzoneButton />
        <ActionToggle />
      </MantineProvider>
    </>
  );
}

export default App;
