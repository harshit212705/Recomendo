import "./css/graph.css";
import Profile from "./profile.js";
import React from "react";

function Graph(props) {
  const users = [];
  for (let i = 1; i <= 104; i++) users.push(i);
  console.log(`Graph.js > ${props.activeUser}`);

  return (
    <div className="graph_container">
      <div className="graph">
        {users.map((id, index) => {
          let profileType = "btn-default";
          if (id === props.activeUser) profileType = "btn-active";
          if (props.friendsAndRecommendations !== null) {
            if (props.friendsAndRecommendations[0].includes(id)) {
              // "id" is a friend
              profileType = "btn-friend";
            }
            if (id in props.friendsAndRecommendations[1]) {
              profileType = "btn-recommendation";
            }
          }
          return (
            <Profile
              key={index}
              userid={id}
              profileType={profileType}
              activeUser={props.activeUser}
              bridge={props.bridge}
              refreshGraph={props.refreshGraph}
              recommendationScore={
                props.friendsAndRecommendations !== null ? props.friendsAndRecommendations[1][id] : 0
              }
            />
          );
        })}
      </div>
    </div>
  );
}

export default Graph;
