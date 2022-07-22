-- name: get_user_by_id
SELECT
  id,
  username
FROM
  auth_user
WHERE
  id = $1;

-- name: get_user_by_username
SELECT
  id,
  username
FROM
  auth_user
WHERE
  username = $1;
