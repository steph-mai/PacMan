import json
import os


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
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("[!] Warning: Highscore file is corrupted or unreadable. "
                  "Starting fresh.")
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

        self.scores.append({"name": safe_name, "score": score})

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
            print(f"[!] Error saving highscores: {e}")
