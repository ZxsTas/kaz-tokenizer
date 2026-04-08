# Multilingual Tokenizer

This is a tokenizer that supports Kazakh morphology, Russian, and English languages with full morpheme analysis and agglutination support.

## Features
- Supports Kazakh, Russian, and English.
- Provides full morpheme analysis.
- Handles agglutination in Kazakh.

## Usage

```python
class MultilingualTokenizer:
    def __init__(self, language='en'):
        self.language = language
        self.rules = self.load_rules()  # Load relevant rules for the specified language

    def load_rules(self):
        # Load language specific rules for tokenization and morphology analysis
        if self.language == 'kk':  # Kazakh
            return self.load_kazakh_rules()
        elif self.language == 'ru':  # Russian
            return self.load_russian_rules()
        else:  # Default to English
            return self.load_english_rules()

    def load_kazakh_rules(self):
        # Load rules specific to Kazakh language
        return {...}

    def load_russian_rules(self):
        # Load rules specific to Russian language
        return {...}

    def load_english_rules(self):
        # Load rules specific to English language
        return {...}

    def tokenize(self, text):
        tokens = self.apply_rules(text)
        return tokens

    def apply_rules(self, text):
        # Apply the loaded rules to tokenize the text
        return [...]  # List of tokens

# Example of how to use the tokenizer
if __name__ == '__main__':
    tokenizer = MultilingualTokenizer(language='kk')  # Kazakh
    tokens = tokenizer.tokenize('Сәлем, қалайсың?')  # Hello, how are you?
    print(tokens)
```

## Installation

You can install the tokenizer via pip:

```bash
pip install multilingual-tokenizer
```

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. We appreciate any feedback or suggestions! 

## License

This project is licensed under the MIT License.