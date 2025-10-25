from pathlib import Path
import os

import easy_client.builders.validator as validator
from  easy_client.utils import get_api_name, get_api_endpoints


def enums_params():
    detect_enums = False
    enum_size = 10
    enum_min_freq = 0.01
    enum_threshold = 0.95
    
    answer = input("Detect enums from string fields? (y/n, default n): ").strip().lower()
    if answer == 'y':
        detect_enums = True
        
        answer = input("Maximal amount of enum values? (default 10): ").strip()
        if answer:
            enum_size = int(answer)
        answer = input("Minimal frequency of enum values? (default 0.01): ").strip()
        if answer:
            enum_min_freq = float(answer)
        answer = input("Threshold for enum detection? (default 0.95): ").strip()
        if answer:
            enum_threshold = float(answer)
    return (detect_enums, enum_size, enum_min_freq, enum_threshold)


def validate(root: Path | None = None):
    print("Create Validation models for collected data...")
    if root is None:
        root = Path(os.getcwd())
        
    # inputs
    api_name = get_api_name()
    endpoints = get_api_endpoints()
    mode, nb, freg, thresh = enums_params()

    # setup
    data_dir = root / api_name / "data" / "raw"
    validation_dir = root / api_name / api_name / "client" / "validate"  # FIXME: use api or something
    
    for file in data_dir.glob("*.json"):
        base_name = os.path.basename(file)
        class_name = os.path.splitext(base_name)[0]
        
        if class_name in endpoints:
            print("Build validation model for", class_name, mode, nb, freg, thresh)
            class_name = class_name[:1].upper() + class_name[1:]
            validator.build_schema_file(json_path=file,
                                        output_path=validation_dir / f"{class_name.lower()}.py",
                                        enums=mode,
                                        max_enum=nb,
                                        min_freq=freg,
                                        threshold=thresh)

if __name__ == "__main__":
    validate()