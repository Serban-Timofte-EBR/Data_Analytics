import pandas as pd

def cleanData(df):
    assert isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Data contains missing values. Cleaning data...")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
        print("Data cleaned successfully.")
    return df


def cleanDataSmartphones(df):
    """
    1. processor:
       - Processor_Speed_GHz: Extracted speed in GHz
       - Processor_Cores: Mapped number of cores based on text (Single Core, Dual Core, etc.)
       - Processor_Chipset: Extracted chipset name (Snapdragon, MediaTek)
       - Original column processor is dropped

    2. price:
       - Converted to numeric by removing non-digit characters.

    3. card:
       - Card_Supported: Binary column, checks for "Supported"
       - Card_Hybrid: Binary column, checks for "Hybrid"
       - Card_Not_Supported: Binary column, checks for "Not Supported"
       - Original column card is dropped

    4. sim:
       - Binary columns created for features like Dual_Sim, Single_Sim, 5G, VoLTE, WiFi, NFC, IR_Blaster, Vo5G
       - Original column sim is dropped

    5. ram:
       - ram_gb: Extracted RAM size in GB
       - inbuilt_storage_gb: Extracted inbuilt storage in GB using regex (\d+)\?GB inbuilt

    6. battery:
       - Extracted battery capacity in mAh

    7. display:
       - display_inches: Extracted display size in inches using regex (\d+\.\d+) inches
       - resolution: Extracted resolution as text

    8. resolution:
       - resolution_width, resolution_height: Split into width and height

    9. camera:
       - camera_primary: Extracted primary camera resolution in MP

    10. Redundant columns removed:
        - ram, battery, display, camera, resolution.
    """
    assert isinstance(df, pd.DataFrame)

    if 'processor' in df.columns:
        df['Processor_Speed_GHz'] = df['processor'].str.extract(r'(\d+\.?\d*)\s?(GHz|GHz Processor)?').iloc[:,0].astype(float)
        core_mapping = {
            'Single Core': 1,
            'Dual Core': 2,
            'Quad Core': 4,
            'Hexa Core': 6,
            'Octa Core': 8,
            'Deca Core': 10,
        }
        df['Processor_Cores'] = (
            df['processor']
            .str.extract(r'(\w+ Core)')[0]
            .map(core_mapping)
            .fillna(0)  # Default to 0 if mapping not found
        )

        # Extract chipset type
        df['Processor_Chipset'] = df['processor'].str.extract(
            r'(Snapdragon|MediaTek|Exynos|Dimensity|Apple|Kirin|Unisoc)')

        # Drop the original `processor` column
        df.drop(columns=['processor'], inplace=True)

    if 'price' in df.columns:
        df['price'] = df['price'].str.replace(r'[^\d]', '', regex=True).astype(float)

    if 'card' in df.columns:
        df['Card_Supported'] = df['card'].str.contains('Supported', na=False).astype(int)
        df['Card_Hybrid'] = df['card'].str.contains('Hybrid', na=False).astype(int)
        df['Card_Not_Supported'] = df['card'].str.contains('Not Supported', na=False).astype(int)
        df.drop(columns=['card'], inplace=True)

    if 'sim' in df.columns:
        df['Dual_Sim'] = df['sim'].str.contains('Dual Sim', na=False).astype(int)
        df['Single_Sim'] = df['sim'].str.contains('Single Sim', na=False).astype(int)
        df['5G'] = df['sim'].str.contains('5G', na=False).astype(int)
        df['VoLTE'] = df['sim'].str.contains('VoLTE', na=False).astype(int)
        df['WiFi'] = df['sim'].str.contains('Wi-Fi', na=False).astype(int)
        df['NFC'] = df['sim'].str.contains('NFC', na=False).astype(int)
        df['IR_Blaster'] = df['sim'].str.contains('IR Blaster', na=False).astype(int)
        df['Vo5G'] = df['sim'].str.contains('Vo5G', na=False).astype(int)
    df.drop(columns=['sim'], inplace=True)

    if 'processor' in df.columns:
        df['Processor_Speed_GHz'] = df['processor'].str.extract(r'(\d+\.?\d*)\s?GHz').astype(float)

    if 'ram' in df.columns:
        df['ram_gb'] = df['ram'].str.extract(r'(\d+)\?GB').astype(float)
        df['inbuilt_storage_gb'] = df['ram'].str.extract(r'(\d+)\?GB inbuilt').astype(float)

    if 'battery' in df.columns:
        df['battery_mAh'] = df['battery'].str.extract(r'(\d+)\?mAh').astype(float)

    if 'display' in df.columns:
        df['display_inches'] = df['display'].str.extract(r'(\d+\.\d+) inches').astype(float)
        df['resolution'] = df['display'].str.extract(r'(\d+\?x\?\d+)')

    if 'camera' in df.columns:
        df['camera_primary'] = df['camera'].str.extract(r'(\d+)\?MP').astype(float)

    if 'resolution' in df.columns:
        df[['resolution_width', 'resolution_height']] = df['resolution'].str.split(r'\?x\?', expand=True).astype(float)

    columns_to_drop = ['ram', 'battery', 'display', 'camera', 'resolution']
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

    print("Smartphones dataset cleaned and processed successfully.")
    return df