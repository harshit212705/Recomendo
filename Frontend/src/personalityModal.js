import { Modal, Button } from "react-bootstrap";
import React, { useState } from "react";
import MBTI_Image1 from "./MyersBriggsTypes1.png";
import MBTI_Image2 from "./MyersBriggsTypes2.png";

function PersonalityModal(props) {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Button variant="link" onClick={handleShow}>
        <span
          style={{
            fontSize: "14px",
            fontWeight: "bold",
            display: "block",
          }}
        >
          Personality Type: {props.personality}
        </span>
      </Button>

      <Modal size="xl" show={show} onHide={handleClose}>
        <Modal.Header style={{ display: "block", textAlign: "center" }}>
          <Modal.Title>MBTI Personality classification</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ display: "block", textAlign: "center" }}>
          <img src={MBTI_Image1} />
          <img src={MBTI_Image2} />
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
}

export default PersonalityModal;
