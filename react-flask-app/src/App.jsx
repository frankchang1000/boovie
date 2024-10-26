import "@mantine/core/styles.css";
import CardsCarousel from "@/components/carousel.tsx";
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { createTheme, MantineProvider } from "@mantine/core";

const theme = createTheme({
  /** Put your mantine theme override here */
});

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <MantineProvider theme={theme}>
        <CardsCarousel />
      </MantineProvider>
    </>
  );
}

export default App;
