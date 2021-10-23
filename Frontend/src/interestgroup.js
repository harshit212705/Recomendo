import "./css/interestgroup.css";
import axios from "axios";
import { useState, useEffect } from "react/cjs/react.development";
import { GET_INTEREST_TAGS } from "./apis.js";

function Tag(props) {
  return <span className="tag">{props.tagname}</span>;
}

function InterestGroup(props) {
  const [tags, settags] = useState([]);
  const getTags = async () => {
    await axios
      .get(GET_INTEREST_TAGS, { params: { userid: props.activeUser } })
      .then((res) => {
        // res.data must be list of tags
        settags(res.data.data);
      })
      .catch((err) => {
        alert(`An error occured while fetching interesttags: ${err}`);
      });
  };
  useEffect(() => {
    console.log(`InterestGroup > getting tags...`);
    getTags();
  }, [props.activeUser]);

  return (
    <div className="interestgroup">
      {tags.map((tag, index) => {
        return <Tag key={index} tagname={tag} />;
      })}
    </div>
  );
}

export default InterestGroup;
