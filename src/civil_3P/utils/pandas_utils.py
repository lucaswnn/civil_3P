import pandas as pd


class PandasUtils:
    @staticmethod
    def rename_or_add_columns(
        df: pd.DataFrame,
        rename_mapping: dict[str, str],
        default_mapping: dict[str, object],
    ) -> None:
        df.rename(columns=rename_mapping, inplace=True)
        for key, value in default_mapping.items():
            if key not in df.columns:
                df[key] = value

    @staticmethod
    def keep_columns(
        df: pd.DataFrame,
        columns_to_keep: list[str],
    ) -> None:
        df.drop(
            columns=[col for col in df.columns if col not in columns_to_keep],
            inplace=True,
        )

    @staticmethod
    def ensure_columns(
        df: pd.DataFrame,
        expected_columns: list[str],
    ) -> None:
        for column in expected_columns:
            if column not in df.columns:
                raise ValueError(f"Missing expected column: {column}")
