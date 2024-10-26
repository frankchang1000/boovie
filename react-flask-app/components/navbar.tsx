import React from "react";
import { Container, Group, Burger } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import classes from "../css/navbar.module.css";
import { ActionToggle } from "./themeselector";
import Logo from "../imgs/logo.svg";

export default function NavBar({ themeMode, setThemeMode }) {
  const [opened, { toggle }] = useDisclosure(false);

  return (
    <header className={classes.header}>
      <Container size="md" className={classes.inner}>
        <div className={classes.logoContainer}>
          <img src={Logo} alt="Logo" width={50} height={50} />
          <h3>Boovies</h3>
        </div>
        <Group>
          <Burger opened={opened} onClick={toggle} hiddenFrom="xs" size="sm" />
          <ActionToggle theme={themeMode} setTheme={setThemeMode} />
        </Group>
      </Container>
    </header>
  );
}
