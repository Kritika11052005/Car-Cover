# Car-Cover
# OLX Web Scraper

A robust Python web scraper built with Playwright to extract product listings from OLX.in. Features multiple fallback strategies, comprehensive error handling, and debugging capabilities.

## Features

- **Multi-Strategy Selector Approach**: Uses multiple CSS selectors to handle OLX's dynamic page structure
- **Robust Error Handling**: Comprehensive error catching and debugging output
- **Anti-Detection Measures**: Realistic browser simulation with proper user agents
- **Fallback Mechanisms**: Multiple extraction strategies if primary selectors fail
- **Debug Mode**: Saves page content for troubleshooting when data extraction fails
- **Flexible Output**: Exports data to CSV with pandas integration
- **Progress Logging**: Real-time feedback on scraping progress

## Requirements

### Python Dependencies
```
playwright>=1.40.0
pandas>=1.5.0
```

### System Requirements
- Python 3.8+
- Chromium browser (installed via Playwright)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/olx-scraper
cd olx-scraper
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers:**
```bash
playwright install chromium
```

## Usage

### Basic Usage
```python
from olx_scraper import fetch_olx_data

# Scrape car covers from OLX
url = "https://www.olx.in/items/q-car-cover"
listings = fetch_olx_data(url)

# Save to CSV
import pandas as pd
df = pd.DataFrame(listings)
df.to_csv("olx_listings.csv", index=False)
```

### Command Line Usage
```bash
python olx_scraper.py
```

### Custom Search Queries
```python
# Different product categories
urls = [
    "https://www.olx.in/items/q-mobile-phone",
    "https://www.olx.in/items/q-laptop", 
    "https://www.olx.in/items/q-bike",
    "https://www.olx.in/items/q-furniture"
]

for url in urls:
    listings = fetch_olx_data(url)
    # Process listings...
```

## Output Format

The scraper extracts the following data for each listing:

| Field | Description | Example |
|-------|-------------|---------|
| Title | Product title/name | "Waterproof Car Cover for Sedan" |
| Price | Listed price | "₹ 1,200" |

### Sample CSV Output
```csv
Title,Price
Waterproof Car Cover for Sedan,₹ 1200
Premium Car Body Cover,₹ 850
UV Protection Car Cover,₹ 2000
Universal Car Cover,₹ 950
```

## Technical Details

### Selector Strategies

The scraper uses multiple fallback strategies to handle OLX's dynamic selectors:

#### Title Selectors (in order of preference):
1. `[data-aut-id='itemTitle']` - Primary OLX selector
2. `._2tW1I` - Legacy class selector
3. `.EKdUR` - Alternative class selector
4. `[data-testid='listing-title']` - Test ID selector
5. `h2 a` - Generic heading link
6. `.title` - Generic title class
7. `a[data-aut-id='itemTitle']` - Link with data attribute

#### Price Selectors (in order of preference):
1. `[data-aut-id='itemPrice']` - Primary OLX price selector
2. `._89yzn` - Legacy price class
3. `.notranslate` - Price display class
4. `[data-testid='listing-price']` - Test ID price selector
5. `.price` - Generic price class
6. `span[data-aut-id='itemPrice']` - Span with data attribute

### Fallback Strategy

If specific selectors fail, the scraper:
1. Looks for listing containers: `[data-aut-id='itemBox']`, `.EKdUR`, `._1kVFD`
2. Searches within each container for title and price elements
3. Uses generic selectors as last resort

## Configuration Options

### Browser Settings
```python
# Modify browser configuration
context = browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    viewport={'width': 1920, 'height': 1080},
    extra_http_headers={
        'Accept-Language': 'en-US,en;q=0.9',
    }
)
```

### Timing Settings
```python
# Adjust wait times
page.goto(url, timeout=60000)  # Page load timeout
page.wait_for_timeout(10000)   # General wait time
page.wait_for_selector("[data-aut-id='itemBox']", timeout=30000)  # Element wait
```

## Troubleshooting

### Common Issues and Solutions

#### 1. No Data Extracted
**Symptoms**: CSV file is empty or contains only headers
**Solutions**:
- Check if OLX has updated their selectors
- Review `debug_page.html` for actual page structure
- Verify the search URL returns results manually
- Check for CAPTCHA or access restrictions

#### 2. Partial Data Extraction
**Symptoms**: Some listings missing titles or prices
**Solutions**:
- OLX uses lazy loading - increase wait times
- Some listings may have different structures
- Check for promoted vs regular listings

#### 3. Rate Limiting / Blocking
**Symptoms**: Page loads but shows blocking message
**Solutions**:
```python
# Add delays between requests
import time
time.sleep(random.uniform(2, 5))

# Rotate user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]
```

#### 4. Playwright Installation Issues
```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium

# For Ubuntu/Debian
sudo apt-get install libnss3-dev libatk-bridge2.0-dev libdrm2-dev libxcomposite-dev libxdamage-dev libxrandr-dev libgbm-dev libxss1-dev libasound2-dev
```

## Debugging

### Enable Debug Mode
The scraper automatically saves debug information when extraction fails:

```python
# Debug files created:
# - debug_page.html: Full page source
# - Console output: Detailed extraction attempts
```

### Manual Debugging
```python
# Add custom debugging
def debug_selectors(page, selectors):
    for selector in selectors:
        elements = page.locator(selector).all()
        print(f"Selector '{selector}': found {len(elements)} elements")
        if elements:
            print(f"  First element text: {elements[0].text_content()[:50]}...")
```

### Inspect Page Structure
```python
# Save and inspect page structure
content = page.content()
with open("page_structure.html", "w", encoding="utf-8") as f:
    f.write(content)

# Check what elements are actually present
all_links = page.locator("a").all()
print(f"Found {len(all_links)} links on page")
```

## Legal and Ethical Considerations

### Usage Guidelines
- **Respect robots.txt**: Check OLX's robots.txt file
- **Rate Limiting**: Add delays between requests to avoid overwhelming servers
- **Terms of Service**: Review OLX's terms of service before scraping
- **Personal Use**: Use scraped data responsibly and for legitimate purposes

### Best Practices
```python
# Implement rate limiting
import time
import random

def respectful_scraping():
    # Random delay between 2-5 seconds
    time.sleep(random.uniform(2, 5))
    
    # Limit concurrent requests
    # Use session management
    # Monitor for blocking signals
```

## Performance Optimization

### Speed Improvements
```python
# Disable images and CSS for faster loading
context = browser.new_context(
    user_agent="Mozilla/5.0...",
    extra_http_headers={'Accept': 'text/html,application/xhtml+xml'}
)

# Use headless mode for production
browser = p.chromium.launch(headless=True)
```

### Memory Management
```python
# Close resources properly
try:
    # Scraping code
    pass
finally:
    page.close()
    context.close()
    browser.close()
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/improvement`
3. **Make changes** and test thoroughly
4. **Update selectors** if OLX changes their structure
5. **Add tests** for new functionality
6. **Submit pull request** with detailed description

### Reporting Issues
When reporting issues, please include:
- Error messages and stack traces
- URL being scraped
- Sample of `debug_page.html` if available
- Python and Playwright versions

## Roadmap

### Planned Features
- [ ] Proxy rotation support
- [ ] Multiple city/location scraping
- [ ] Advanced filtering options
- [ ] Database storage options
- [ ] Scheduled scraping with cron jobs
- [ ] Email notifications for new listings
- [ ] Price tracking and alerts

### Version History
- **v1.0.0**: Initial release with basic scraping
- **v1.1.0**: Added multi-selector fallback strategies
- **v1.2.0**: Enhanced error handling and debugging
- **v1.3.0**: Added configuration options


## Disclaimer

This tool is for educational and research purposes. Users are responsible for complying with OLX's terms of service and applicable laws. The developers are not responsible for misuse of this tool.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/olx-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/olx-scraper/discussions)
- **Email**: your.email@example.com

---

**⚠️ Important Note**: Web scraping terms and website structures change frequently. This scraper may require updates to maintain functionality. Always verify that your usage complies with the website's terms of service and local laws.
