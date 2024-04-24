# Content Retriever

The `ContentRetriever` class is designed to extract information from web page elements related to credit card cashback offers. It utilizes various methods to parse and extract relevant data, such as cashback details, card types, and eligible purchase categories.

## Installation

To use the `ContentRetriever` class, you need to install the required libraries:

```bash
pip install nltk beautifulsoup4 textdistance numpy
```

## Usage

Here's how you can use the `ContentRetriever` class to extract information from web page elements:

```python
from retriever import ContentRetriever
from bs4 import BeautifulSoup
from presets import objectives

# Initialize the ContentRetriever
retriever = ContentRetriever()

# Example HTML element
html_element = '<div>Kaspi Gold 10% магазин</div>'
el = BeautifulSoup(html_element, 'html.parser')

# Retrieve information about available cashback
cashback_info = retriever.retrieve_info_from_element(el)

# Retrieve the type of credit card
card_type = retriever.retrieve_card_from_element(el)

# Retrieve the cashback percentage
cashback_percent = retriever.retrieve_percent_from_element(el)

# retrieve the type of purchase category
purchase_category = retriever.retrieve_objective_from_text(cashback_info)

# Print the extracted information
print("Cashback Info:", cashback_info)
print("Card Type:", card_type)
print("Cashback Percent:", cashback_percent)
print("Purchase Category Family:", objectives[purchase_category])
```

```bash
Cashback Info: Kaspi Gold 10% магазин. 
Card Type: gold
Cashback Percent: 10%
Purchase Category Family: ['онлайн покупки', 'магазин', 'роуминг', 'apple pay', 'sumsung pay', 'google pay', 'музыка', 'геймер', 'apple', 'netflix', 'spotify', 'google', 'интернет магазин', 'markets', 'игровые сервисы', 'онлайн кино', 'онлайн музыка']
```

Make sure to have the `presets.py` and `utils.py` files available, which are assumed to contain the `cards` and `objectives` presets and the `AhoCorasick` utility class, respectively. Adjust the usage example to match your specific requirements and data sources.
