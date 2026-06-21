import re
import logging

logger = logging.getLogger(__name__)

METRIC_PATTERNS = {
    'body_fat_percent': [
        r'body\s*fat\s*[:%]?\s*([\d.,]+)\s*%?',
        r'fat\s*mass\s*[:%]?\s*([\d.,]+)\s*%?',
        r'fat\s*percentage\s*[:%]?\s*([\d.,]+)\s*%?',
        r'体脂肪率\s*[:%]?\s*([\d.,]+)\s*%?',
    ],
    'muscle_mass_percent': [
        r'muscle\s*mass\s*[:%]?\s*([\d.,]+)\s*%?',
        r'skeletal\s*muscle\s*[:%]?\s*([\d.,]+)',
        r'muscle\s*percentage\s*[:%]?\s*([\d.,]+)\s*%?',
        r'筋肉量\s*[:%]?\s*([\d.,]+)',
    ],
    'muscle_mass_kg': [
        r'muscle\s*mass\s*[:\s]*([\d.,]+)\s*kg',
        r'skeletal\s*muscle\s*[:\s]*([\d.,]+)\s*kg',
        r'筋肉量\s*[:\s]*([\d.,]+)\s*kg',
    ],
    'bmi': [
        r'bmi\s*[:%]?\s*([\d.,]+)',
        r'body\s*mass\s*index\s*[:%]?\s*([\d.,]+)',
    ],
    'water_percent': [
        r'water\s*[:%]?\s*([\d.,]+)\s*%?',
        r'body\s*water\s*[:%]?\s*([\d.,]+)\s*%?',
        r'hydration\s*[:%]?\s*([\d.,]+)\s*%?',
        r'水分\s*[:%]?\s*([\d.,]+)\s*%?',
    ],
    'visceral_fat': [
        r'visceral\s*fat\s*[:%]?\s*([\d.,]+)',
        r'内臓脂肪\s*[:%]?\s*([\d.,]+)',
    ],
    'bone_mass_kg': [
        r'bone\s*mass\s*[:\s]*([\d.,]+)\s*kg',
        r'bone\s*weight\s*[:\s]*([\d.,]+)\s*kg',
        r'骨量\s*[:\s]*([\d.,]+)\s*kg',
    ],
    'bone_mass_percent': [
        r'bone\s*mass\s*[:%]?\s*([\d.,]+)\s*%?',
        r'bone\s*percentage\s*[:%]?\s*([\d.,]+)\s*%?',
    ],
    'basal_metabolism_kcal': [
        r'basal\s*metabolism\s*[:\s]*([\d.,]+)\s*kcal',
        r'bmr\s*[:\s]*([\d.,]+)',
        r'基础代谢\s*[:\s]*([\d.,]+)',
        r'基础代謝\s*[:\s]*([\d.,]+)',
    ],
    'body_age': [
        r'body\s*age\s*[:%]?\s*([\d.,]+)',
        r'metabolic\s*age\s*[:%]?\s*([\d.,]+)',
        r'身体年齢\s*[:%]?\s*([\d.,]+)',
    ],
    'weight_kg': [
        r'weight\s*[:\s]*([\d.,]+)\s*kg',
        r'体重\s*[:\s]*([\d.,]+)\s*kg',
    ],
    'protein_percent': [
        r'protein\s*[:%]?\s*([\d.,]+)\s*%?',
        r'蛋白质\s*[:%]?\s*([\d.,]+)\s*%?',
    ],
    'subcutaneous_fat': [
        r'subcutaneous\s*fat\s*[:%]?\s*([\d.,]+)\s*%?',
        r'皮下脂肪\s*[:%]?\s*([\d.,]+)\s*%?',
    ],
    'obesity_grade': [
        r'obesity\s*grade\s*[:%]?\s*([\d.,]+)',
        r'肥胖等级\s*[:%]?\s*([\d.,]+)',
    ],
}


def parse_number(value):
    try:
        return float(value.replace(',', '.'))
    except (ValueError, AttributeError):
        return None


def parse_body_composition(text):
    if not text:
        return {}

    metrics = {}
    text_lower = text.lower()

    for metric, patterns in METRIC_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                value = parse_number(match.group(1))
                if value is not None:
                    metrics[metric] = value
                    break

    logger.info(f'Parsed metrics: {metrics}')
    return metrics
