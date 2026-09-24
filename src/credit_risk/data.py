"""Load, clean and split the UCI Default of Credit Card Clients data."""

import pandas as pd
from sklearn.model_selection import train_test_split

from credit_risk.config import load_config

TARGET = "default"

RENAMES = {
    "default payment next month": TARGET,
    "PAY_0": "PAY_1",
}

EDUCATION_REGROUP = {0: 4, 5: 4, 6: 4}
MARRIAGE_REGROUP = {0: 3}

SPLITS = ("train", "validation", "test")
SPLIT_FILE = "split.parquet"


def load_raw(config_name: str = "uci_taiwan") -> pd.DataFrame:
    """Return the raw dataset with the real column names as the header.

    Columns are renamed per RENAMES; values are left untouched.
    """
    config = load_config(config_name)
    path = config["paths"]["raw_dir"] / config["source"]["raw_file"]
    df = pd.read_excel(path, header=1)
    return df.rename(columns=RENAMES)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy indexed by ID, with undocumented EDUCATION and MARRIAGE codes
    merged into their "other" category."""
    df = df.set_index("ID")
    df["EDUCATION"] = df["EDUCATION"].replace(EDUCATION_REGROUP)
    df["MARRIAGE"] = df["MARRIAGE"].replace(MARRIAGE_REGROUP)
    return df


def make_split(
    df: pd.DataFrame, config_name: str = "uci_taiwan", overwrite: bool = False
) -> pd.Series:
    """Assign each ID to train, validation or test, stratified on the target,
    and save the assignment to the processed data directory.

    Raises FileExistsError if a split is already saved, unless overwrite=True.
    """
    config = load_config(config_name)
    shares = config["split"]
    seed = shares["seed"]
    path = config["paths"]["processed_dir"] / SPLIT_FILE

    if path.exists() and not overwrite:
        raise FileExistsError(
            f"{path} already exists; pass overwrite=True to replace it."
        )

    rest, test = train_test_split(
        df.index, test_size=shares["test"], stratify=df[TARGET], random_state=seed
    )
    validation_share = shares["validation"] / (1 - shares["test"])
    _, validation = train_test_split(
        rest,
        test_size=validation_share,
        stratify=df.loc[rest, TARGET],
        random_state=seed,
    )

    assignment = pd.Series("train", index=df.index, name="split")
    assignment.loc[validation] = "validation"
    assignment.loc[test] = "test"

    path.parent.mkdir(parents=True, exist_ok=True)
    assignment.to_frame().to_parquet(path)
    return assignment


def load_splits(
    df: pd.DataFrame, include_test: bool = False, config_name: str = "uci_taiwan"
) -> dict[str, pd.DataFrame]:
    """Return {split name: rows of df} using the saved assignment.

    The test set is only returned when include_test=True.
    """
    config = load_config(config_name)
    assignment = pd.read_parquet(config["paths"]["processed_dir"] / SPLIT_FILE)["split"]
    names = SPLITS if include_test else SPLITS[:2]
    return {name: df.loc[assignment.index[assignment == name]] for name in names}
