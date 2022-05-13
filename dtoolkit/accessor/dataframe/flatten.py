from __future__ import annotations

import pandas as pd


def flatten(
    df: pd.DataFrame,
    name: str | int = None,
    dropna: bool = True,
) -> pd.Series:
    """
    Return a Series collapsed into one dimension.

    Parameters
    ----------
    dropna: bool, default True
        The result doesn't include NA values.

    Examples
    --------
    >>> import dtoolkit.accessor
    >>> import pandas as pd
    >>> data = {
    ...     "Generation I": [
    ...         "Pocket Monsters: Red and Green",
    ...         "Pocket Monsters: Blue",
    ...         "Pokémon Red and Blue",
    ...         "Pokémon Yellow"
    ...     ],
    ...     "Generation II": [
    ...         "Pokémon Gold and Silver",
    ...         "Pokémon Crystal"
    ...     ],
    ...     "Generation III": [
    ...         "Pokémon Ruby and Sapphire",
    ...         "Pokémon FireRed and LeafGreen",
    ...         "Pokémon Emerald"
    ...     ],
    ...     "Generation IV": [
    ...         "Pokémon Diamond and Pearl",
    ...         "Pokémon Platinum",
    ...         "Pokémon HeartGold and SoulSilver"
    ...     ],
    ...     "Generation V": [
    ...         "Pokémon Black and White",
    ...         "Pokémon Black 2 and White 2"
    ...     ],
    ...     "Generation VI": [
    ...         "Pokémon X and Y",
    ...         "Pokémon Omega Ruby and Alpha Sapphire"
    ...     ],
    ...     "Generation VII": [
    ...         "Pokémon Sun and Moon",
    ...         "Pokémon Ultra Sun",
    ...         "Pokémon: Let's Go, Pikachu! and Let's Go, Eevee!"
    ...     ],
    ...     "Generation VIII": [
    ...         "Pokémon Sword and Shield",
    ...         "Pokémon Brilliant Diamond and Shining Pearl",
    ...         "Pokémon Legends: Arceus"
    ...     ],
    ...     "Generation IX": [
    ...         "Pokémon Scarlet and Violet"
    ...     ]
    ... }
    >>> df = pd.DataFrame.from_dict(data, orient="index").T
    >>> df
                         Generation I  ...               Generation IX
    0  Pocket Monsters: Red and Green  ...  Pokémon Scarlet and Violet
    1           Pocket Monsters: Blue  ...                        None
    2            Pokémon Red and Blue  ...                        None
    3                  Pokémon Yellow  ...                        None
    [4 rows x 9 columns]
    >>> df.flatten(name="Pokémon Game List")
    0                       Pocket Monsters: Red and Green
    1                              Pokémon Gold and Silver
    2                            Pokémon Ruby and Sapphire
    3                            Pokémon Diamond and Pearl
    4                              Pokémon Black and White
    5                                      Pokémon X and Y
    6                                 Pokémon Sun and Moon
    7                             Pokémon Sword and Shield
    8                           Pokémon Scarlet and Violet
    9                                Pocket Monsters: Blue
    10                                     Pokémon Crystal
    11                       Pokémon FireRed and LeafGreen
    12                                    Pokémon Platinum
    13                         Pokémon Black 2 and White 2
    14               Pokémon Omega Ruby and Alpha Sapphire
    15                                   Pokémon Ultra Sun
    16         Pokémon Brilliant Diamond and Shining Pearl
    18                                Pokémon Red and Blue
    20                                     Pokémon Emerald
    21                    Pokémon HeartGold and SoulSilver
    24    Pokémon: Let's Go, Pikachu! and Let's Go, Eevee!
    25                             Pokémon Legends: Arceus
    27                                      Pokémon Yellow
    Name: Pokémon Game List, dtype: object
    """

    result = pd.Series(
        df.to_numpy().flatten(),
        name=name,
    )

    return result.dropna() if dropna else result
