
import React from "react";
// reactstrap components
import { Container, Row, Col } from "reactstrap";

export default function Typography() {
  return (
    <div className="section section-typo">
      <img alt="..." className="path" src={require("assets/img/path1.png")} />
      <img
        alt="..."
        className="path path1"
        src={require("assets/img/path3.png")}
      />
      <Container>
        <h3 className="title">Reviews</h3>
        <div id="typography">
          <Row>
            <Col md="12">
              <div className="typography-line">
                <span>Success Text</span>
                <p className="text-success">
                  I will be the leader of a company that ends up being worth
                  billions of dollars, because I got the answers...
                </p>
              </div>
              <div className="typography-line">
                <span>Warning Text</span>
                <p className="text-warning">
                  I will be the leader of a company that ends up being worth
                  billions of dollars, because I got the answers...
                </p>
              </div>
              <div className="typography-line">
                <span>Danger Text</span>
                <p className="text-danger">
                  I will be the leader of a company that ends up being worth
                  billions of dollars, because I got the answers...
                </p>
              </div>
              
            </Col>
          </Row>
        </div>
        <div className="space-50" />
        {/*<div id="images">
          <h3 className="mb-5">Images</h3>
          <Row>
            <Col sm="3" xs="6">
              <small className="d-block text-uppercase font-weight-bold mb-4">
                Image
              </small>
              <img
                alt="..."
                className="img-fluid rounded shadow"
                src={require("assets/img/ryan.jpg")}
                style={{ width: "150px" }}
              />
            </Col>
            <Col sm="3" xs="6">
              <small className="d-block text-uppercase font-weight-bold mb-4">
                Circle Image
              </small>
              <img
                alt="..."
                className="img-fluid rounded-circle shadow"
                src={require("assets/img/james.jpg")}
                style={{ width: "150px" }}
              />
            </Col>
            <Col className="mt-5 mt-sm-0" sm="3" xs="6">
              <small className="d-block text-uppercase font-weight-bold mb-4">
                Raised
              </small>
              <img
                alt="..."
                className="img-fluid rounded shadow-lg"
                src={require("assets/img/lora.jpg")}
                style={{ width: "150px" }}
              />
            </Col>
            <Col className="mt-5 mt-sm-0" sm="3" xs="6">
              <small className="d-block text-uppercase font-weight-bold mb-4">
                Circle Raised
              </small>
              <img
                alt="..."
                className="img-fluid rounded-circle shadow-lg"
                src={require("assets/img/mike.jpg")}
                style={{ width: "150px" }}
              />
            </Col>
          </Row>
  </div>*/}
      </Container>
    </div>
  );
}
