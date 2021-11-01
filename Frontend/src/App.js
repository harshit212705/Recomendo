import "./css/App.css";
import Graph from "./graph.js";
import Panel from "./panel.js";
// import PersonalityModal from "./personalityModal.js";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { GET_FRIENDS_AND_RECOMMENDATIONS } from "./apis.js";

function App() {
  const [activeUser, setactiveUser] = useState(null);
  const [friendAndRecommendations, setfriendAndRecommendations] =
    useState(null);
  const [graphrerender, updategraphrerender] = useState(0);

  const refreshGraph = () => {
    updategraphrerender(graphrerender + 1);
  };

  const bridgeGraphToApp = (userid) => {
    setactiveUser(userid);
    setfriendAndRecommendations(null);
    console.log(`App.js > setting active user to: ${userid}`);
  };
  const bridgePanelToApp = () => {
    showFriendsAndRecommendations();
    // other code, maybe, for transferring other data/signal from panel to graph
  };

  const showFriendsAndRecommendations = async () => {
    await axios
      .get(GET_FRIENDS_AND_RECOMMENDATIONS + `?userid=${activeUser}`)
      .then((res) => {
        //This res.data must be a list of list as: [[Friends], [Recommendations]]
        let list = res.data.data;
        if (list !== null) setfriendAndRecommendations(list);
      })
      .catch((err) => {
        alert(
          `An error occured while fetching Friends and Recommendations: ${err}`
        );
      });
  };

  useEffect(() => {
    if (activeUser !== null) {
      console.log(`------------------refreshing graph---------------`);
      showFriendsAndRecommendations();
    }
  }, [graphrerender]);

  console.log(`App.js > rendering App`);
  return (
    <div className="App">
      <h1>Recommending Friends on Personality and Connections</h1>
      <div className="content">
        {/* <PersonalityModal /> */}
        <Graph
          activeUser={activeUser}
          bridge={bridgeGraphToApp}
          friendsAndRecommendations={friendAndRecommendations}
          refreshGraph={refreshGraph}
        />
        <Panel
          activeUser={activeUser}
          friendsAndRecommendations={friendAndRecommendations}
          bridge={bridgePanelToApp}
          refreshGraph={refreshGraph}
        />
      </div>
    </div>
  );
}

export default App;
