import Post from "./post.js";
import "./css/savedpost.css";
import { useState, useEffect } from "react/cjs/react.development";
import axios from "axios";
import { GET_POSTS, DELETE_POST } from "./apis.js";

function SavedPost(props) {
  const [posts, setposts] = useState([]);
  const getPosts = async () => {
    await axios
      .get(GET_POSTS + `?userid=${props.activeUser}`)
      .then((res) => {
        // res.data must be array of object: {timestamp, body}
        let posts = res.data.data;
        console.log(`SavedPosts: ${posts}`);
        setposts(posts);
      })
      .catch((err) => {
        alert(`An error occured while fetching posts: ${err}`);
      });
  };

  const addNewPost = (newpost) => {
    setposts([...posts, newpost]);
  };

  const deletepost = (postid) => {
    axios
      .get(DELETE_POST, {
        params: {
          userid: props.activeUser,
          postid: postid,
        },
      })
      .then(() => {
        setposts(posts.filter((post) => post.postid !== postid));
      })
      .catch((err) => {
        alert(`An error occured while deleting post: ${err}`);
      });
  };

  useEffect(() => {
    console.log(`SavedPosts.js > getting posts...`);
    getPosts();
  }, [props.activeUser]);

  console.log(`Savedpost.js > newpost: ${props.newpost}`);
  useEffect(() => {
    if (props.newpost !== null) {
      console.log(`SavedPosts.js > adding newpost...`);
      addNewPost(props.newpost);
    }
  }, [props.newpost]);

  return (
    <div className="savedpost">
      {posts.map((post, index) => {
        return (
          <Post
            key={index}
            timestamp={post.timestamp}
            body={post.body}
            postid={post.postid}
            deletepost={deletepost}
          />
        );
      })}
    </div>
  );
}

export default SavedPost;
