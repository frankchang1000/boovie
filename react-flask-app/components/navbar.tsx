import React from "react";
import { Container, Group, Burger } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { MantineLogo } from "@mantinex/mantine-logo";
import classes from "../css/navbar.module.css";
import { ActionToggle } from "./themeselector";

export default function NavBar({ themeMode, setThemeMode }) {
  const [opened, { toggle }] = useDisclosure(false);

  return (
    <header className={classes.header}>
      <Container size="md" className={classes.inner}>
        <MantineLogo size={28} />
        <Group>
          <Burger opened={opened} onClick={toggle} hiddenFrom="xs" size="sm" />
          <ActionToggle theme={themeMode} setTheme={setThemeMode} />
        </Group>
      </Container>
    </header>
  );
}