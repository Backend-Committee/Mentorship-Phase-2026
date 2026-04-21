import json
import os

from inbuddy.BodyCompositionDataExtractionEngine import (
    BodyCompositionDataExtractionEngine,
)
from inbuddy.Logger import Logger

if __name__ == "__main__":
    logger = Logger()
    image_file = "./assets/inbody1.jpg"
    extractor = BodyCompositionDataExtractionEngine()
    if os.path.exists(image_file):
        result = extractor.extract(image_file)
        if result:
            with open("output.json", "w") as f:
                json.dump({"data": result}, f, indent=4)
            logger.log("Successfully saved to output.json")
    else:
        logger.error("File not found.")
