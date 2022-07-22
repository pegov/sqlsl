-- name: get_game_by_id
SELECT
  id,
  nickname,
  score
FROM
  game
WHERE
  id = $1;

-- name: get_games_by_score
SELECT
  id,
  nickname,
  score
FROM
  game
WHERE
  score = $1;
