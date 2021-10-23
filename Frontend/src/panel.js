import "./css/panel.css";
import UserInfo from "./userinfo.js";
import SavedPost from "./savedpost.js";
import CreatePost from "./createpost.js";
import InterestGroup from "./interestgroup.js";
import { useState } from "react/cjs/react.development";

function Lable(props) {
  return (
    <div>
      <span
        style={{
          fontWeight: "bold",
          display: "block",
          fontSize: "14px",
          margin: "0",
          padding: "0",
        }}
      >
        {props.lablename}
      </span>
    </div>
  );
}

function Panel(props) {
  const [newpost, setnewpost] = useState(null);

  console.log(`Panel.js > ${props.activeUser}`);

  // const showFriendsAndRecommendations = async () => {
  //   await axios
  //     .get(GET_FRIENDS_AND_RECOMMENDATIONS + `?userid=${props.activeUser}`)
  //     .then((res) => {
  //       //This res.data must be a list of list as: [[Friends], [Recommendations]]
  //       let list = res.data;
  //       props.bridge(list);
  //     })
  //     .catch((err) => {
  //       alert(
  //         `An error occured while fetching Friends and Recommendations: ${err}`
  //       );
  //     });
  // };

  if (props.activeUser === null) {
    return <div className="empty-panel"></div>;
  }

  return (
    <div className="panel-container">
      <div className="panel">
        <UserInfo
          activeUser={props.activeUser}
          showFriendsAndRecommendations={props.bridge}
        />
        <Lable lablename="Interest Groups" />
        <InterestGroup activeUser={props.activeUser} />
        <Lable lablename="Posts" />
        <SavedPost activeUser={props.activeUser} newpost={newpost} />
        <CreatePost
          activeUser={props.activeUser}
          updateNewPost={setnewpost}
          refreshGraph={props.refreshGraph}
        />
      </div>
    </div>
  );
}

export default Panel;
