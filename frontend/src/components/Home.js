import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import QueryList from "./QueryList";
import NewQueryModal from "./NewQueryModal";

import axios from "axios";
import { API_URL } from "../constants";

class Home extends Component {
  state = {
    queries: []
  };

  componentDidMount() {
    this.resetState();
  }

  getQueries = () => {
    axios.get(API_URL).then(res => this.setState({ queries: res.data }));
  };

  resetState = () => {
    this.getQueries();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <QueryList
              queries={this.state.queries}
              resetState={this.resetState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <NewQueryModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Home;
