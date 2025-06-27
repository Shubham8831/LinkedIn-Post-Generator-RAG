import json
import pandas as pd


class FewShotPosts:
    """
    A utility class to load, categorize, and filter LinkedIn posts for few-shot training.

    Attributes:
        df (pd.DataFrame): DataFrame containing post data and computed features.
        unique_tags (set): Set of all unique tags across loaded posts.
    """
    def __init__(self, file_path="data/processed_posts.json"):
        """
        Initialize FewShotPosts by loading data from the given JSON file.

        Args:
            file_path (str): Path to the processed posts JSON file.
        """
        # DataFrame will hold the normalized post data
        self.df = None
        # Set of unique tags across all posts
        self.unique_tags = None
        # Load and prepare data
        self.load_post(file_path)

    def load_post(self, file_path):
        """
        Load JSON posts, normalize into DataFrame, compute length categories, and extract unique tags.

        Args:
            file_path (str): Path to the processed posts JSON file.
        """
        # Read raw JSON list of posts
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)

        # Convert list of dicts into pandas DataFrame
        df = pd.json_normalize(posts)

        # Add a new column 'length' by categorizing 'line_count'
        df["length"] = df["line_count"].apply(self.length_category)

        # Expand the 'tags' lists into a series to gather all tags
        all_tags = df["tags"].explode()
        # Store unique tags for later retrieval
        self.unique_tags = set(all_tags)

        # Assign the processed DataFrame to the instance
        self.df = df

    def length_category(self, line_count):
        """
        Categorize post length based on number of lines.

        Args:
            line_count (int): Number of lines in the post.
        Returns:
            str: 'Short' if <5, 'Medium' if 5–10, else 'Long'.
        """
        if line_count < 5:
            return "Short"  # Very brief post
        elif 5 <= line_count <= 10:
            return "Medium"  # Moderate-length post
        else:
            return "Long"  # Extended content

    def get_tags(self):
        """
        Retrieve all unique tags found in the dataset.

        Returns:
            set: Unique tag values.
        """
        return self.unique_tags

    def get_filtered_post(self, length, language, tags):
        """
        Filter posts by length category, language, and tags.

        Args:
            length (str): Desired length category ('Short', 'Medium', 'Long').
            language (str): Language code to filter posts (e.g., 'English').
            tags (str or list): Single tag or list of tags to match.

        Returns:
            list: Filtered posts as a list of dictionaries.
        """
        # Ensure tags is always a list for consistent filtering
        if isinstance(tags, str):
            tags = [tags]

        def has_any_tag(tag_list):
            """
            Check if any of the desired tags appear in a post's tag list.

            Args:
                tag_list (list): Tags associated with a post.
            Returns:
                bool: True if at least one desired tag is found.
            """
            return any(t in tag_list for t in tags)

        # Apply all filter criteria to DataFrame
        df_filtered = self.df[
            self.df["tags"].apply(has_any_tag) &  # Tag filter
            (self.df["language"] == language) &  # Language filter
            (self.df["length"] == length)       # Length category filter
        ]

        # Convert filtered DataFrame slice back to list of dicts
        return df_filtered.to_dict(orient='records')


if __name__ == "__main__":
    # Example usage
    fs = FewShotPosts()
    # Retrieve medium-length English posts tagged with 'Job Search'
    posts = fs.get_filtered_post("Medium", "English", ["career advice"])
    print(posts)
