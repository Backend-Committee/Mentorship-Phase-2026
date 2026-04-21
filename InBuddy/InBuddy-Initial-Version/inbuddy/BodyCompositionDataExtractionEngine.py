import os
import sys
import time

import PIL.Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

from inbuddy.Logger import Logger

load_dotenv()


class BodyCompositionDataExtractionEngine:
    def __init__(self):
        self.logger = Logger("BodyCompositionExtractor")
        self.models_to_try = [
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
        ]

        API_KEY = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=API_KEY)

    def __setUpConfig(self):
        return types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "weight": {"type": "NUMBER"},
                    "bmi": {"type": "NUMBER"},
                    "body_fat_percentage": {"type": "NUMBER"},
                    "muscle_mass": {"type": "NUMBER"},
                    "skeletal_muscle_mass": {"type": "NUMBER"},
                    "total_body_water": {"type": "NUMBER"},
                    "fat_mass": {"type": "NUMBER"},
                    "lean_body_mass": {"type": "NUMBER"},
                    "basal_metabolic_rate": {"type": "NUMBER"},
                    "visceral_fat_level": {"type": "NUMBER", "nullable": True},
                    "bone_mineral_content": {"type": "NUMBER", "nullable": True},
                    "age": {"type": "INTEGER", "nullable": True},
                    "gender": {"type": "STRING", "nullable": True},
                    "height_cm": {"type": "NUMBER", "nullable": True},
                    # Segmental analysis is a nested object
                    "segmental_lean_analysis": {
                        "type": "OBJECT",
                        "properties": {
                            "right_arm": {"type": "NUMBER"},
                            "left_arm": {"type": "NUMBER"},
                            "trunk": {"type": "NUMBER"},
                            "right_leg": {"type": "NUMBER"},
                            "left_leg": {"type": "NUMBER"},
                        },
                        "nullable": True,
                    },
                },
                "required": ["weight", "bmi", "body_fat_percentage", "muscle_mass"],
            },
        )

    def __requestModelAPI(self, image_path, config, model_name):
        prompt = """
    SYSTEM: You are a medical data extraction expert specialized in Bioelectrical Impedance Analysis (BIA) reports.
    TASK:
    1. Identify the 'Body Composition Analysis' table and 'Segmental Lean Analysis' graphs.
    2. Locate the numeric values corresponding to the labels provided in the schema.
    3. For values like 'Skeletal Muscle Mass' and 'Muscle Mass', strictly distinguish between them.
    4. If a value is shown as a bar graph without a number, estimate the value based on the 100% (Normal) mark.
    5. If the image is blurry, use the 'Total Body Water' and 'Fat Free Mass' to cross-verify the 'Muscle Mass' calculation.
    6. Return ONLY a valid JSON object following the provided schema.
    """
        img = PIL.Image.open(image_path)
        response = self.client.models.generate_content(
            model=model_name,
            contents=[prompt, img],
            config=config,
        )
        return response.parsed

    def __wait_nSeconds(self, n):
        for i in range(n, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(i))
            sys.stdout.flush()
            time.sleep(1)

    def __503ErrorHandler(self, model_name):
        self.logger.error(f"Server Busy (503) for {model_name}. Trying fallback...")
        if model_name == self.models_to_try[-1]:
            self.logger.error(
                "All models are currently unavailable. Please wait 1-2 minutes."
            )
            self.__wait_nSeconds(120)
            self.logger.log("\nRetrying now...")
            return True  # Signal to retry from the first model after waiting
        return False  # Signal to try the next model immediately

    def extract(self, image_path):
        config = self.__setUpConfig()

        model_index = 0
        while model_index < len(self.models_to_try):
            try:
                self.logger.log(
                    f"Attempting extraction with {self.models_to_try[model_index]}..."
                )
                return self.__requestModelAPI(
                    image_path, config, self.models_to_try[model_index]
                )
            except Exception as e:
                if "503" in str(e):
                    if self.__503ErrorHandler(self.models_to_try[model_index]):
                        model_index = 0
                    else:
                        model_index += 1
                else:
                    self.logger.error(
                        f"Error with {self.models_to_try[model_index]}: {e}"
                    )
                    model_index += 1
        return None
