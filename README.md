# The Orb Weaver Project

*A spinner of webs and a weaver for devs.*

The repository is a tool for crawling and weaving through the web. It houses various methods for scraping and navigating the web with code, leaving as minimal a footprint as possible. The project leverages advanced techniques like dynamic IP changes, headless browsing, and custom user-agent settings to ensure stealth and efficiency in web scraping activities.

## Features

- **Dynamic IP Management**: Automatically changes IP addresses using PIA VPN to bypass IP-based blocking.
- **Headless Mode**: Supports running Chrome in headless mode for efficient background operations without a GUI.
- **Custom User-Agent**: Sets a random user-agent for each session to mimic different devices and avoid detection.
- **SSL Proxy Support**: Configures Chrome WebDriver to use HTTPS/SSL proxies for secure and private connections.
- **Minimal Footprint**: Designed to leave the smallest possible footprint to avoid triggering anti-scraping mechanisms.

## Installation

### Prerequisites

- Python 3.10 or higher.
- Google Chrome or Chromium.
- Selenium WebDriver.

### Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/orb-weaver.git
    cd orb-weaver
    ```

2. **Install Dependencies**:
    - It's recommended to set up a virtual environment with poetry:
      ```bash
      poetry lock
      ```
    - Install the required Python packages:
      ```bash
      poetry install --no-cache
      ```

## Usage

This repository contains code designed to enhance web scraping and automated testing by simulating human interactions within a web browser. By mimicking human behavior, these tools aim to evade detection mechanisms employed by many modern websites.

Firstly, a driver must be initialised. Here’s how to initialize and use the `OrbDriver` to perform web scraping:

```python
from orb.webdriver.orb_driver import OrbDriver

# Create an instance of OrbDriver
orb_driver = OrbDriver()

# Get the initialized WebDriver
driver = orb_driver.get_webdriver()

# Now you can use `driver` to navigate and scrape websites
```

### Changing IP Address

To change your IP address, an active subscription to PIA VPN is required; using the OrbDriver:

```python
orb_driver.change_ip_address()
```

### Setting User Agents

Rotating through a random assortment of user agents:

```python
orb_driver.set_user_agent()
```

### Spoofing requests

Requests can be spoofed by passing in different user aganets to return a response:

```python
from bs4 import BeautifulSoup
from orb.scraper.utils import spoof_request

response = spoof_request(url=driver.current_url, use_proxies=False)

if not response:
        raise ValueError("Failed to retrieve content from driver's current URL")

soup = BeautifulSoup(response.content, 'html.parser')
```

### Human-Like Typing

The slow_type function allows you to type text into a web element character by character with a random delay between keystrokes, optionally followed by an "Enter" key press. This simulates the way a human would type into a form field or search box.

**Example Usage**

```python
from selenium.webdriver.common.by import By

# Assuming 'driver' is an already initialized WebDriver instance
element = driver.find_element(By.ID, 'input-field-id')
slow_type(element, "Hello, world!", send_keys=True)
```

### Randomised Clicking

The human_clicking function performs clicks that include random mouse movements before the actual click, simulating more natural cursor movement.

**Example Usage**

```python
from selenium.webdriver.common.by import By

# Assuming 'driver' is an already initialized WebDriver instance
target_element = driver.find_element(By.ID, 'button-id')
human_clicking(driver, target_element)
```

### Random Mouse Movements

The perform_random_mouse_movements function creates random mouse movements within the browser window, which can help in making automated scripts less detectable.

**Example Usage**

```python
# Assuming 'driver' is an already initialized WebDriver instance
perform_random_mouse_movements(driver)
```

### Window Scrolling

The window_scroll function randomly scrolls through a webpage within specified limits, mimicking how a human might scroll through a long article or webpage.

**Example Usage**

```python
# Assuming 'driver' is an already initialized WebDriver instance
window_scroll(driver, scroll_range=(0, 50))  # Scroll between the top of the page and the midpoint
```

### Changing the Viewport Size

The change_viewport_size function adjusts the size of the browser window to random dimensions within specified ranges, which can vary the browser's fingerprint.

**Example Usage**

```python
# Assuming 'driver' is an already initialized WebDriver instance
change_viewport_size(driver)
```
