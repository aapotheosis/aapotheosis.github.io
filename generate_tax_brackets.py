#!/usr/bin/env python3
""" 
Generate tax bracket data from canatax package.

This script uses the canatax package to fetch current Canadian tax brackets 
and outputs them in the JSON format format expected by the RRSP Loan Maximizer calculator.

Usage:
    pip install canatax
    python generate_tax_brackets.py

Output:
    Creates a file named tax_brackets_YYYY.json (e.g., 'tax_brackets_2025.json") 
    where YYYY is the current tax year.

The output format matches the structure expected by script.js:
{
    "year": 2025,
    "federal":
        { "min": 0, "max": 57375, "rate": 0.15 },
        ...
    ],
    "provincial": {
        "AB": {
            "name": "Alberta",
            "brackets": [
                { "min": 0,"max": 151234, "rate": 0.10 },
                ...
            ]
        },
        ...
    }
}
"""

import json
import sys
from datetime import datetime
from math import inf

# Province codes and their full names
PROVINCE_NAMES = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NS': 'Nova Scotia',
    'NT': 'Northwest Territories',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
}

# Map province codes to class names in canatax
PROVINCE_TO_CLASS = {
    'AB': 'AlbertaIncomeTaxRate',
    'BC': 'BritishColumbiaIncomeTaxRate',
    'MB': 'ManitobaIncomeTaxRate',
    'NB': 'NewBrunswickIncomeTaxRate',
    'NL': 'NewfoundlandIncomeTaxRate',
    'NS': 'NovaScotiaIncomeTaxRate',
    'NT': 'NorthwestTerritoriesIncomeTaxRate',
    'NU': 'NunavutIncomeTaxRate',
    'ON': 'OntarioIncomeTaxRate',
    'PE': 'PEIIncomeTaxRate',
    'QC': 'QuebecIncomeTaxRate',
    'SK': 'SaskatchewanIncomeTaxRate',
    'YT': 'YukonIncomeTaxRate',
}


def format_brackets(tax_rate_obj):
    """
    Convert canatax bracket tuples to our dictionary format.
    
    canatax returns brackets as list of tuples: (rate_percentage, max_amount)
    where rate is a percentage (15, 20.5) not decimal (0.15, 0.205)
    
    We convert to: { "min": min, "max": max, "rate": rate_decimal }
    where rate is converted to decimal (0.15, 0.205)
    """
    formatted = []
    brackets = tax_rate_obj.brackets
    
    for i, (rate_pct, max_val) in enumerate(brackets):
        # Calculate min from previous bracket's max
        if i == 0:
            min_val = 0
        else:
            min_val = brackets[i-1][1]  # Previous bracket's max
        
        # Convert rate from percentage to decimal
        rate_decimal = rate_pct / 100
        
        # Handle infinity for top bracket
        if max_val == float('inf'):
            max_val_serializable = "Infinity"
        else:
            max_val_serializable = max_val
        
        formatted.append({
            "min": min_val,
            "max": max_val_serializable,
            "rate": rate_decimal
        })
    
    return formatted


def get_federal_brackets(tax_rate_classes):
    """
    Get federal tax brackets from canatax.

    Args:
        tax_rate_classes: dict with tax rate class objects

    Returns list of bracket dictionaries.
    """
    try:
        fed = tax_rate_classes['FederalIncomeTaxRate']()
        return format_brackets(fed)
    except Exception as e:
        print(f"Error fetching federal brackets: {e}")
        return None
    

def get_provincial_brackets(tax_rate_classes, province_code):
    """
    Get provincial tax brackets from canatax for a specific province.

    Args:
        tax_rate_classes: dict with tax rate class objects
        province_code: 2-letter province code (AB, BC, etc.)

    Returns dict with 'name' and 'brackets' keys.
    """
    try:
        # Get the class name from our mapping
        class_name = PROVINCE_TO_CLASS.get(province_code)
        if not class_name or class_name not in tax_rate_classes:
            print(f"No tax rate class found for {province_code}")
            return None
        
        # Instantiate and get brackets
        prov_obj = tax_rate_classes[class_name]()
        return {
            "name": PROVINCE_NAMES.get(province_code, province_code),
            "brackets": format_brackets(prov_obj)
        }
    except Exception as e:
        print(f"Error fetching brackets for {province_code}: {e}")
        return None
    

def generate_tax_data():
    """
    Generate complete tax bracket data using canatax.

    Returns dict with 'year', 'federal', and 'provincial' keys.
    """
    try:
        from canatax.rates.income.tax_rates import rates_2025
    except ImportError:
        print("Error: canatax package not installed.")
        print("Please install it with 'pip install canatax'.")
        sys.exit(1)

    # Build a dictionary of all tax rate classes
    tax_rate_classes = {
        'FederalIncomeTaxRate': rates_2025.FederalIncomeTaxRate,
        'AlbertaIncomeTaxRate': rates_2025.AlbertaIncomeTaxRate,
        'BritishColumbiaIncomeTaxRate': rates_2025.BritishColumbiaIncomeTaxRate,
        'ManitobaIncomeTaxRate': rates_2025.ManitobaIncomeTaxRate,
        'NewBrunswickIncomeTaxRate': rates_2025.NewBrunswickIncomeTaxRate,
        'NewfoundlandIncomeTaxRate': rates_2025.NewfoundlandIncomeTaxRate,
        'NovaScotiaIncomeTaxRate': rates_2025.NovaScotiaIncomeTaxRate,
        'NorthwestTerritoriesIncomeTaxRate': rates_2025.NorthwestTerritoriesIncomeTaxRate,
        'NunavutIncomeTaxRate': rates_2025.NunavutIncomeTaxRate,
        'OntarioIncomeTaxRate': rates_2025.OntarioIncomeTaxRate,
        'PEIIncomeTaxRate': rates_2025.PEIIncomeTaxRate,
        'QuebecIncomeTaxRate': rates_2025.QuebecIncomeTaxRate,
        'SaskatchewanIncomeTaxRate': rates_2025.SaskatchewanIncomeTaxRate,
        'YukonIncomeTaxRate': rates_2025.YukonIncomeTaxRate,
    }

    # Use 2025 as the year (from rates_2025 module)
    year = 2025

    print(f"Generating tax brackets for year: {year}")

    # Get federal brackets
    print("Fetching federal brackets...")
    federal = get_federal_brackets(tax_rate_classes)
    if federal is None:
        print("Failed to get federal brackets")
        sys.exit(1)

    # Get provincial brackets for all provinces
    provincial = {}
    for province_code in PROVINCE_NAMES.keys():
        print(f"Fetching brackets for {province_code}...")
        brackets = get_provincial_brackets(tax_rate_classes, province_code)
        if brackets:
            provincial[province_code] = brackets
        else:
            print(f"Failed to get brackets for {province_code}")

    return {
        "year": year,
        "federal": federal,
        "provincial": provincial
    }


def main():
    """Main entry point."""
    print("=" * 50)
    print("RRSP Loan Maximizer - Tax Bracket Generator")
    print("=" * 50)
    print()

     # Generate tax data
    tax_data = generate_tax_data()

     # Create output filename
    year = tax_data["year"]
    output_file = f"tax_brackets_{year}.json"

    # Write to file
    print()
    print(f"Writing to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tax_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {output_file}")
    print()
    print("Tax data summary:")
    print(f"    - Year: {year}")
    print(f"    - Federal brackets: {len(tax_data['federal'])}")
    print(f"    - Provincial brackets: {len(tax_data['provincial'])}")
    print()
    print("The calculator will automatically load this file when opened.")
    print()


# Alternative  function to print brackets in JavaScript format
def print_js_format():
    """
    Print tax brackets in JavaScript format for manual copy/past.end=
    
    This is useful if you if you want to add the brackets directly to script.js
    instead of loading them from a JSON file.
    """
    try:
        import canatax
    except ImportError:
        print("Error: canatax package not installed.")
        sys.exit(1)

    tax_data = generate_tax_data()
    year = tax_data["year"]

    print(f"\n// Tax brackets for {year} (generated by canatax)")
    print(f"// Add this to the TAX_DATA object in script.js\n")

    # Federal brackets
    print(f"{year}: {{")
    print("  federal: [")
    for bracket in tax_data["federal"]:
        max_val = "Infinity" if bracket["max"] == "Infinity" else bracket["max"]
        print(f"    {{ min: {bracket['min']}, max: {max_val}, rate: {bracket['rate']} }},")
    print("  ],")

    # Provincial brackets
    print("  provincial: {")
    for code, data in tax_data["provincial"].items():
        print(f"    {code}: {{")
        print(f"      name: '{data['name']}',")
        print("      brackets: [")
        for bracket in data["brackets"]:
            max_val = "Infinity" if bracket["max"] == "Infinity" else bracket["max"]
            print(f"        {{ min: {bracket['min']}, max: {max_val}, rate: {bracket['rate']} }},")
        print("      ]")
        print("    },")
    print("  }")
    print("}")


if __name__ == "__main__":
    # Check for command line arguemnts
    if len(sys.argv) > 1 and sys.argv[1] == "--js":
        print_js_format()
    else:
        main()