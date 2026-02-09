# RRSP Loan Maximizer | Canadian Tax Calculator 🇨🇦

A powerful web-based calculator to help Canadian taxpayers maximize their RRSP loan strategy by calculating optimal loan amounts based on real Canadian federal and provincial tax brackets.

## Features

- **Interactive Tax Calculator**: Real-time calculations based on your income and province
- **Current Tax Data**: Uses automatically updated Canadian tax brackets for 2025
- **Multi-Province Support**: Comprehensive tax bracket data for all Canadian provinces
- **Modern UI**: Clean, responsive design with help panel and FAQs
- **Offline Ready**: Works fully in your browser with locally loaded tax data
- **Historical Data Fallback**: Includes 2024 tax data as backup

## What is an RRSP Loan Maximizer?

An RRSP (Registered Retirement Savings Plan) loan strategy helps you maximize tax-deductible contributions. This calculator determines the optimal loan amount by calculating your marginal tax rate and potential tax savings.

## Quick Start

### Option 1: Use Online
Visit your GitHub Pages site at [aapotheosis.github.io](https://aapotheosis.github.io)

### Option 2: Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/aapotheosis/aapotheosis.github.io.git
   cd aapotheosis.github.io
   ```

2. Start a local web server:
   ```bash
   # Using Python 3
   python -m http.server 3000
   
   # Then visit: http://localhost:3000
   ```

## Project Structure

```
├── index.html                 # Main application page
├── script.js                  # Calculator logic and UI interactions
├── styles.css                 # Responsive styling
├── generate_tax_brackets.py   # Script to update tax data for new years
├── tax_brackets_2025.json     # Current tax bracket data
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Updating Tax Brackets for New Years

The project includes a Python script to automatically fetch and update Canadian tax brackets for new tax years:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the generator script:
   ```bash
   python generate_tax_brackets.py
   ```

3. This creates/updates `tax_brackets_YYYY.json` with the latest tax data

## Technical Details

### Frontend
- **HTML5**: Semantic markup and accessibility features
- **CSS3**: Modern styling with responsive design
- **JavaScript (ES6+)**: Dynamic calculations and interactions

### Backend (Data Generation)
- **Python 3**: Script to fetch and format tax data
- **canatax Package**: Reliable source for Canadian tax bracket data

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## How to Use

1. Select your province from the dropdown
2. Enter your current annual income
3. View your marginal tax rate and calculated tax savings
4. Adjust the loan amount to see different scenarios
5. Use the Help panel for detailed explanations

## Troubleshooting

**"Tax data not found" error:**
- Regenerate tax brackets by running `python generate_tax_brackets.py`
- Ensure `tax_brackets_2025.json` exists in the project root

**Local server won't start:**
```bash
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace XXXX with PID)
taskkill /F /PID XXXX
```

## Contributing

Feel free to submit issues and enhancement requests!

## Disclaimer

This calculator is for educational and planning purposes only. It does not constitute financial, tax, or investment advice. Consult with a qualified tax professional or financial advisor before making any financial decisions related to RRSP loans.

## License

Open source - feel free to use, modify, and distribute

## Author

aapotheosis

---

**Last Updated**: February 2026  
**Current Tax Year Data**: 2025
