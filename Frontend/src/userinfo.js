import "./css/userinfo.css";
import "./css/profile.css";
import axios from "axios";
import PersonalityModal from "./personalityModal.js";
import { useState, useEffect } from "react/cjs/react.development";
import { GET_USERINFO } from "./apis.js";

function UserInfo(props) {
  const [userinfo, setuserinfo] = useState({});
  const getUserInfo = async () => {
    await axios
      .get(GET_USERINFO + `?userid=${props.activeUser}`)
      .then((res) => {
        // res.data must be object: {username, personality}
        setuserinfo(res.data);
      })
      .catch((err) => {
        alert(`An error occured while fetching userinfo: ${err}`);
      });
  };

  useEffect(() => {
    console.log(`UserInfo > getting userinfo...`);
    getUserInfo();
  }, [props.activeUser, props.friendAndRecommendations]);

  return (
    <div className="userinfo">
      <span style={{ fontWeight: "bold", display: "block" }}>
        {userinfo.username}
      </span>
      <PersonalityModal personality={userinfo.personality} />
      <span style={{ fontSize: "14px", fontWeight: "bold", display: "block" }}>
        Age: {userinfo.age}
      </span>
      <button
        type="button"
        className="btn btn-md btn-friend hvr-wobble-skew"
        onClick={props.showFriendsAndRecommendations}
      >
        <div
          className="btn-md btn-friend"
          style={{ display: "inline-block", margin: "auto 10px" }}
        >
          Friends
        </div>

        <div
          className="btn-md btn-recommendation"
          style={{
            display: "inline-block",
            margin: "auto 10px",
            padding: "5px",
            borderRadius: "5px",
          }}
        >
          Recommendations
        </div>
      </button>
    </div>
  );
}

export default UserInfo;
