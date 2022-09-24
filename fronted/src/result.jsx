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
    Alert,
    Blockquote,
    ActionIcon,
  } from "@mantine/core";
  
  import { AiOutlineCloud } from "react-icons/ai";
  import { IoIosArrowBack } from "react-icons/io";
  
  export default function Result(props) {
    return (
      <Container style={{ position: "relative" }}>
        <Container
          style={{
            padding: "50px",
            height: "100%",
            width: "95%",
            display: "inline-block",
          }}
        >
          <ActionIcon
            variant="light"
            size="xl"
            style={{ margin: 20 }}
            onClick={() => {
              props.setSection(1);
            }}
          >
            <IoIosArrowBack size={16} />
          </ActionIcon>
          <Card shadow="sm" radius="md" style={{ padding: 70 }}>
            <Center style={{ marginBottom: 20 }}>
              <Title size={30} weight={500}>
                {<AiOutlineCloud />} &nbsp; {props.prompt}
              </Title>
            </Center>
            <Card.Section>
              <Center>
                <Image
                  radius={10}
                  fit="contain"
                  width={712}
                  height={712}
                  src={props.image}
                />
              </Center>
            </Card.Section>
          </Card>
        </Container>
        <Container style={{ display: "inline-block", verticalAlign: "top" }}>
          <Container
            style={{
              width: "5%",
              position: "absolute",
              bottom: "33%",
              width: 270,
            }}
          >
            <Card shadow="sm" radius="md">
              <Image
                radius={10}
                fit="contain"
                width={212}
                height={212}
                src={props.qr}
              />
              <Text
                size="xl"
                color="dimmed"
                align="center"
                style={{ marginTop: 15 }}
              >
                #OpenDayUTEC
              </Text>
              <Title size={20} align="center" style={{ marginTop: 10 }}>
                Compartelo en tus redes
              </Title>
            </Card>
          </Container>
        </Container>
      </Container>
    );
  }