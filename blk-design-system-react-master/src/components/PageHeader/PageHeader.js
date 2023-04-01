import React from "react";


// reactstrap components
import { Container } from "reactstrap";
import { Row } from "reactstrap";
import { Col } from "reactstrap";
import { Input } from "reactstrap";
import { FormGroup } from "reactstrap";


export default function PageHeader() {
  return (
    <div className="page-header header-filter">
      <div className="squares square1" />
      <div className="squares square2" />
      <div className="squares square3" />
      <div className="squares square4" />
      <div className="squares square5" />
      <div className="squares square6" />
      <div className="squares square7" />
      <Container>
        <div className="content-center brand">
          <h1 className="h1-seo">Review Scope</h1>
          Dwell into the realm of unbiased and authentic product reviews 
          <h3 className="d-none d-sm-block">
            
          </h3>
          <Col lg="12" sm="10">
            <FormGroup className="has-success">
              <Input
                className="form-control-success"
                defaultValue="Enter Product Link"
                type="text"
              />
            </FormGroup>
          </Col>

        </div>
      </Container>
    </div>
  );
}
