import "@mantine/core/styles.css";
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { createTheme, MantineProvider } from "@mantine/core";
import { DropzoneButton } from "../components/upload";
import { CardsCarousel } from "../components/carousel";
import { ActionToggle } from "../components/themeSelector";

const theme = createTheme({
  /** Put your mantine theme override here */
});

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <MantineProvider theme={theme}>
        <CardsCarousel />
        <DropzoneButton />
        <ActionToggle />
      </MantineProvider>
    </>
  );
}

export default App;
