import json
import os
import logging

logger = logging.getLogger("pacman")


class HighScoreManager:
    """
    Manages the loading, validating, and saving of the top 10 player
    scores using a JSON file.
    """

    def __init__(self, filepath: str = "highscores.json") -> None:
        """
        Initialize the highscore manager.

        Args:
            filepath (str): The relative or absolute path to the
            JSON save file.
        """
        self.filepath = filepath
        self.scores: list[dict[str, str | int]] = self.load_scores()

    def load_scores(self) -> list[dict[str, str | int]]:
        """
        Load scores from the JSON file.
        Returns an empty list if the file is missing or
        corrupted to prevent crashes.

        Returns:
            list[dict[str, str | int]]: A list of dictionaries containing
            'name' and 'score'.
        """
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                logger.warning(f"Highscore root is not a list "
                               f"(got {type(data).__name__}). "
                               f"Starting fresh.")
                return []

            valid_scores: list[dict[str, str | int]] = []
            for item in data:
                if isinstance(
                        item, dict) and "name" in item and "score" in item:
                    try:
                        score_val = int(item["score"])

                        if score_val < 0:
                            logger.warning(
                                f"Highscore rejected: negative score "
                                f"({score_val}) for '{item.get('name')}'.")
                            continue

                        if score_val > 999999:
                            logger.warning(
                                f"Highscore cheat detected: impossibly high "
                                f"({score_val}) for '{item.get('name')}'."
                                " Clamped to 999999")
                            score_val = 999999

                        raw_name = str(item["name"])
                        safe_name = "".join(
                            c for c in raw_name
                            if c.isalnum() or c.isspace()
                        )[:10]

                        if raw_name != safe_name:
                            logger.warning(
                                f"Highscore sanitized: name '{raw_name}' "
                                f"changed to '{safe_name}'.")

                        if not safe_name.strip():
                            safe_name = "Anonymous"
                            logger.warning(
                                "Highscore sanitized: empty/invalid name "
                                "replaced by 'Anonymous'.")

                        valid_scores.append({
                            "name": safe_name,
                            "score": score_val
                        })
                    except (ValueError, TypeError):
                        continue

            return valid_scores

        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Highscore file is corrupted or unreadable ({e}). "
                           f"Starting fresh.")
            return []

    def add_score(self, player_name: str, score: int) -> None:
        """
        Add a new score, filter the name, sort the leaderboard,
        and keep only the top 10.

        Args:
            player_name (str): The raw input name from the player.
            score (int): The final score achieved.
        """
        safe_name = "".join(c for c in player_name if
                            c.isalnum() or c.isspace())[:10]

        if not safe_name.strip():
            safe_name = "Anonymous"

        safe_score = max(0, int(score))
        self.scores.append({"name": safe_name, "score": safe_score})

        self.scores.sort(key=lambda x: int(x["score"]), reverse=True)

        self.scores = self.scores[:10]

        self.save_scores()

    def save_scores(self) -> None:
        """
        Write the current top scores back to the JSON file safely.
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(self.scores, file, indent=4)
        except IOError as e:
            logger.error(f"Error saving highscores to disk: {e}")
            raise IOError
