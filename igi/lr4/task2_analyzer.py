"""
Purpose: Text analysis using Regular Expressions, inheritance, and Mixins.
Lab Work: 4
Version: 1.0
Developer: Ivan Safonau
Date: 2026-04-07
"""

import re
import os
import zipfile
from exceptions_validators import InvalidStudentDataError 

class ArchiveMixin:
    """Mixin to provide archiving capabilities for result files."""
    def create_zip(self, file_to_zip: str, zip_name: str):
        """Creates a zip archive and prints information about it."""
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(file_to_zip, os.path.basename(file_to_zip), compresslevel=5)
        
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            info = zipf.getinfo(os.path.basename(file_to_zip))
            print(f"[ZIP INFO] File: {info.filename}, Size: {info.file_size} bytes, Compressed: {info.compress_size} bytes")


class BaseTextProcessor:
    """Base class for text processing."""
    def __init__(self, content: str = ""):
        self._content = content # Dynamic attribute

    @property
    def content(self):
        """Getter for raw text."""
        return self._content

    @content.setter
    def content(self, value):
        """Setter for raw text."""
        self._content = value

    def read_from_file(self, filename: str):
        """Reads text from a file."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found.")
        with open(filename, 'r', encoding='utf-8') as f:
            self.content = f.read()


class TextAnalyzer(BaseTextProcessor, ArchiveMixin):
    """Advanced text analyzer with regex capabilities."""
    
    # Static attribute
    ANALYSIS_COMPLETED_COUNT = 0

    def __init__(self, content: str = ""):
        # super() usage
        super().__init__(content)
        self.results = []

    def perform_general_analysis(self):
        """Standard task: count sentences, types, average lengths, and smileys."""
        text = self.content
        
        # 1. Sentence counts by type
        narrative = len(re.findall(r'[^!?.]+\.', text))
        interrogative = len(re.findall(r'[^!?.]+\?', text))
        exclamatory = len(re.findall(r'[^!?.]+\!', text))
        total_sentences = narrative + interrogative + exclamatory

        # 2. Average lengths
        words = re.findall(r'\b\w+\b', text)
        avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
        
        # Symbols in sentences (only words counted)
        avg_sent_len = sum(len(w) for w in words) / total_sentences if total_sentences else 0

        # 3. Smileys count
        # Regex explanation: [;:] (one of) + [-]* (any minus) + ([\(\)\[\]])\1* (at least one identical bracket)
        smileys = re.findall(r'[;:][-]*([\(\)\[\]])\1*', text)
        
        res = [
            f"Total sentences: {total_sentences}",
            f"Narrative: {narrative}, Interrogative: {interrogative}, Exclamatory: {exclamatory}",
            f"Avg sentence length (chars in words): {avg_sent_len:.2f}",
            f"Avg word length: {avg_word_len:.2f}",
            f"Smileys found: {len(smileys)}"
        ]
        self.results.extend(res)
        return res

    def perform_variant_analysis(self):
        """Individual variant tasks logic."""
        text = self.content
        variant_res = ["\n--- Variant Results ---"]

        # 1. Sentences with spaces, digits, and punctuation
        pattern = r'[^.!?]*[\s][^.!?]*[\d][^.!?]*[.,!?;:][^.!?]*[.!?]'
        complex_sents = re.findall(pattern, text)
        variant_res.append(f"Sentences with spaces, digits, and punctuation: {len(complex_sents)}")

        # 2. Date regex dd/mm/yyyy (1600-9999)
        date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(1[6-9]\d{2}|[2-9]\d{3})\b'
        dates = re.findall(date_pattern, text)
        variant_res.append(f"Valid dates found: {['/'.join(d) for d in dates]}")

        # 3. Uppercase and Lowercase count
        upper = len(re.findall(r'[A-ZА-Я]', text))
        lower = len(re.findall(r'[a-zа-я]', text))
        variant_res.append(f"Case count: Upper={upper}, Lower={lower}")

        # 4. First word with 'z' and its index
        words = re.findall(r'\b\w+\b', text)
        z_word = next(((i+1, w) for i, w in enumerate(words) if 'z' in w.lower()), (None, None))
        variant_res.append(f"First 'z' word: {z_word[1]} at position {z_word[0]}")

        # 5. Exclude words starting with 'a'
        clean_text = re.sub(r'\b[aAаА]\w*\b', '', text).strip()
        variant_res.append("Text with words starting with 'a' removed (saved to file).")

        self.results.extend(variant_res)
        TextAnalyzer.ANALYSIS_COMPLETED_COUNT += 1
        return clean_text

    def save_results(self, filename: str):
        """Saves analysis results to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.results))

    def __str__(self):
        """Magic method: string representation."""
        return f"TextAnalyzer containing {len(self.content)} characters. Analysis runs: {self.ANALYSIS_COMPLETED_COUNT}"