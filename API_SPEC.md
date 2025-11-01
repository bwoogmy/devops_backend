# Twitter Clone API Specification

Base URL: `http://localhost:8000/api/v1`

## Endpoints

### Create Post
**POST** `/posts`

Request:
```json
{
  "content": "Hello world!",
  "author": "username"
}
```

Response: `201 Created`

### Get All Posts
**GET** `/posts?limit=50&offset=0`

### Get Single Post
**GET** `/posts/{post_id}`

### Delete Post
**DELETE** `/posts/{post_id}`

### Like Post
**POST** `/posts/{post_id}/like?user_identifier=username`

### Unlike Post
**DELETE** `/posts/{post_id}/like?user_identifier=username`
