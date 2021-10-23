import "./css/createpost.css";
import "./css/profile.css";
import axios from "axios";
import { useState } from "react/cjs/react.development";
import { ADD_NEW_POST } from "./apis.js";

const getDateTime = () => {
  const obj = new Date();
  const day = obj.getDate(),
    month = obj.getMonth() + 1,
    year = obj.getFullYear(),
    time = obj.toLocaleTimeString("it-IT");

  return `${day}/${month}/${year} | ${time}`;
};

function CreatePost(props) {
  const [newpost, setnewpost] = useState("");

  const addNewPost = async (newpost) => {
    let post = {
      userid: props.activeUser,
      // timestamp: getDateTime(),
      body: newpost.trim(),
      // postid: Date.now(),
    };

    if (post.body !== '') {
      await axios
      .post(ADD_NEW_POST, post)
      .then((res) => {
        console.log("Data posted successfully to server!");
        post.postid = res.data.postid;
        post.timestamp = res.data.timestamp;
        props.updateNewPost(post);
        props.refreshGraph();
      })
      .catch((e) => {
        console.log(`error while posting data to server: ${e}`);
      });
      setnewpost("");
    }
    else {
      alert('Type something before posting!!')
    }
  };

  return (
    <div className="createpost form">
      <input
        className="input-post"
        placeholder="What's on your mind?"
        onChange={(e) => {
          setnewpost(e.target.value);
        }}
        value={newpost}
        type="text"
      ></input>
      <button
        className="btn-circle hvr-forward"
        type="button"
        onClick={() => addNewPost(newpost)}
        style={{ backgroundColor: "#F5F5F5" }}
      >
        <i className="fa fa-arrow-circle-right fa-lg"></i>
      </button>
    </div>
  );
}

export default CreatePost;
