import "./css/profile.css";
import axios from "axios";
import { ADD_FRIEND, REMOVE_FRIEND } from "./apis.js";

function Profile(props) {
  const handleProfileClick = (e) => {
    if (props.activeUser === props.userid) return;
    props.bridge(props.userid);
  };
  const addOrRemoveFriend = (e) => {
    let operation =
      props.profileType === "btn-friend" ? REMOVE_FRIEND : ADD_FRIEND;
    axios
      .get(operation, {
        params: {
          userid: props.userid,
          activeUser: props.activeUser,
        },
      })
      .then((res) => {
        console.log(`profile.js > operation done successfully.`);
        props.refreshGraph();
      })
      .catch((e) => console.log(`profile.js > ${e}`));
  };

  return (
    <div className="profile">
      <button
        type="button"
        className={`btn btn-circle hvr-pop ${props.profileType}`}
        onClick={handleProfileClick}
      >
        <i
          className="far fa-smile"
          style={{ fontSize: "28px", display: "block" }}
        ></i>
        <span style={{ fontSize: "10px", display: "block" }}>
          {props.userid}
        </span>
      </button>
      <div
        className="tooltip-container"
        style={{ display: "inline-block", position: "absolute" }}
      >
        <button
          type="button"
          className={`friendstatus btn btn-sm 	hvr-pulse`}
          style={{
            display:
              props.activeUser === props.userid || props.activeUser === null
                ? "none"
                : "",
            backgroundColor:
              props.profileType === "btn-friend" ? "#FF0000" : "#3DB2FF",
          }}
          onClick={addOrRemoveFriend}
        >
          {props.profileType === "btn-friend" ? "-" : "+"}
        </button>
        <span
          className={`recommendation-score btn btn-sm`}
          style={{
            display:
              props.profileType === "btn-recommendation" ? "block" : "none",
          }}
        >
          {props.recommendationScore}
        </span>
      </div>
    </div>
  );
}

export default Profile;
