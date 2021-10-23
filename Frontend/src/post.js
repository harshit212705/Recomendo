import "./css/post.css";

function Post(props) {
  return (
    <div className="post">
      <div className="post-header">
        <span>{props.timestamp}</span>
        <button
          className="btn btn-xs btn-danger hvr-buzz-out"
          onClick={() => props.deletepost(props.postid)}
        >
          Delete
        </button>
      </div>
      <div className="post-body">
        <p>{props.body}</p>
      </div>
    </div>
  );
}

export default Post;
