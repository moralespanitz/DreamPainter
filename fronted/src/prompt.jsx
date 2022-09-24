import {
  Card,
  Image,
  Text,
  Badge,
  Button,
  Group,
  Container,
  Center,
  Title,
  LoadingOverlay,
} from "@mantine/core";
import { Input } from "@mantine/core";
import { useState } from "react";
import { AiFillCloud } from "react-icons/ai";
import axios from "axios";

export const Prompt = (props) => {
  const [prompt, setPrompt] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    console.log(prompt);
    setLoading(true);
    if (prompt === "") {
      alert("Ingresa una oración para ejecutar la operacion");
      return setLoading(false);
    }
    await axios({
      method: "post",
      url: "http://34.121.85.44:5000/generate",
      data: {
        prompt: prompt,
      },
    })
      .then((data) => {
        setLoading(false);
        props.setImage(data.data.image_cdn_url);
        props.setPrompt(data.data.prompt);
        props.setQr(data.data.qr_cdn_url);
        props.setSection(2);
      })
      .catch(() => setLoading(false));
  }

  return (
    <Container style={{ padding: "50px" }}>
      <LoadingOverlay visible={loading} overlayBlur={2} />
      <Card shadow="sm" radius="md" withBorder>
        <Card.Section>
          <Image
            src="https://utec.edu.pe/sites/default/files/styles/1920x500/public/cabecera_ciencia_computacion.jpg"
            height={300}
            alt="Norway"
          />
        </Card.Section>
        <Container style={{ paddingBottom: 20 }}>
          <Center style={{ marginTop: 15 }}>
            <Title order={1}> Dream Painter </Title>
          </Center>

          <Text size="sm" color="dimmed" align="center">
            With Fjord Tours you can explore more of the magical fjord
            landscapes with tours and activities on and around the fjords of
            Norway
          </Text>
        </Container>

        <Input
          icon={<AiFillCloud />}
          placeholder="Mi sueño es ... "
          onChange={(e) => setPrompt(e.target.value)}
        />

        <Button
          variant="light"
          color="blue"
          fullWidth
          mt="md"
          radius="md"
          style={{ marginTop: 50 }}
          onClick={() => {
            handleSubmit();
          }}
        >
          ¡Soñar!
        </Button>
      </Card>
    </Container>
  );
};