class OCRService:
    _reader = None

    @classmethod
    def get_reader(cls, languages=None):
        import easyocr

        if cls._reader is None:
            if languages is None:
                from django.conf import settings
                languages = getattr(settings, 'EASYOCR_LANGUAGES', ['en'])
            cls._reader = easyocr.Reader(languages, gpu=False)
        return cls._reader

    @staticmethod
    def extract_text(image_path, languages=None):
        reader = OCRService.get_reader(languages)
        results = reader.readtext(image_path, paragraph=True)
        texts = [text for (_, text, confidence) in results]
        return ' '.join(texts)
